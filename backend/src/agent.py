"""
Day 9 – E-commerce Voice Agent (Cart + Checkout)

Brand: Zepto

Features:
- Voice-based shopping assistant using Murf Falcon TTS.
- Small developer-themed catalog (mugs, t-shirts, hoodies, accessories).
- Tools:
    - list_products: search & filter catalog
    - add_to_cart_from_results: add item by index from last search
    - remove_from_cart: remove item from cart by index
    - show_cart: summarize current cart
    - checkout_cart: create an order from cart, persist to JSON
    - get_last_order_summary: answer "What did I just buy?"
- Orders persisted to backend/shared-data/day9_orders.json
"""

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional

from dotenv import load_dotenv
from pydantic import Field

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    WorkerOptions,
    cli,
    function_tool,
    RunContext,
)

from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("day9-ecommerce")
logging.basicConfig(level=logging.INFO)

load_dotenv(".env.local")

BRAND_NAME = "Zepto"
CURRENCY = "INR"

# -----------------------------
# Paths & Files
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "shared-data"))
CATALOG_FILE = os.path.join(DATA_DIR, "day9_catalog.json")
ORDERS_FILE = os.path.join(DATA_DIR, "day9_orders.json")


# -----------------------------
# Default Catalog
# -----------------------------
DEFAULT_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "mug-001",
        "name": "Stoneware Coffee Mug",
        "description": "Matte finish stoneware mug, 350ml, perfect for morning chai or coffee.",
        "price": 399,
        "currency": CURRENCY,
        "category": "mug",
        "color": "white",
        "tags": ["coffee", "minimal", "office"],
    },
    {
        "id": "mug-002",
        "name": "Midnight Code Mug",
        "description": "Black ceramic mug with glow-in-the-dark code pattern.",
        "price": 549,
        "currency": CURRENCY,
        "category": "mug",
        "color": "black",
        "tags": ["developer", "dark-theme"],
    },
    {
        "id": "tee-001",
        "name": "Debug Mode T-shirt",
        "description": "Unisex cotton tee with 'In Debug Mode' print.",
        "price": 899,
        "currency": CURRENCY,
        "category": "tshirt",
        "color": "black",
        "sizes": ["S", "M", "L", "XL"],
        "tags": ["developer", "casual"],
    },
    {
        "id": "tee-002",
        "name": "Coffee & Code T-shirt",
        "description": "Beige tee with minimal coffee + code icon.",
        "price": 799,
        "currency": CURRENCY,
        "category": "tshirt",
        "color": "beige",
        "sizes": ["M", "L"],
        "tags": ["coffee", "minimal"],
    },
    {
        "id": "hoodie-001",
        "name": "Night Owl Hoodie",
        "description": "Black fleece hoodie for late-night coding sessions.",
        "price": 1599,
        "currency": CURRENCY,
        "category": "hoodie",
        "color": "black",
        "sizes": ["M", "L", "XL"],
        "tags": ["warm", "hoodie", "developer"],
    },
    {
        "id": "hoodie-002",
        "name": "Zepto Logo Hoodie",
        "description": "Navy blue hoodie with small Zepto chest logo.",
        "price": 1399,
        "currency": CURRENCY,
        "category": "hoodie",
        "color": "navy",
        "sizes": ["S", "M", "L"],
        "tags": ["brand", "minimal"],
    },
    {
        "id": "accessory-001",
        "name": "Aluminium Laptop Stand",
        "description": "Adjustable height laptop stand, silver finish.",
        "price": 1299,
        "currency": CURRENCY,
        "category": "accessory",
        "color": "silver",
        "tags": ["ergonomic", "office"],
    },
    {
        "id": "accessory-002",
        "name": "Mechanical Keyboard - Blue Switches",
        "description": "Compact 87-key mech keyboard with blue switches.",
        "price": 2999,
        "currency": CURRENCY,
        "category": "accessory",
        "color": "black",
        "tags": ["keyboard", "mechanical"],
    },
]


def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CATALOG, f, indent=2, ensure_ascii=False)
        logger.info("Created default Day 9 catalog at %s", CATALOG_FILE)

    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)
        logger.info("Created empty Day 9 orders file at %s", ORDERS_FILE)


def load_catalog() -> List[Dict[str, Any]]:
    ensure_data_files()
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_orders() -> List[Dict[str, Any]]:
    ensure_data_files()
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_orders(orders: List[Dict[str, Any]]) -> None:
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2, ensure_ascii=False)


def generate_order_id() -> str:
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    orders = load_orders()
    return f"ORD-{ts}-{len(orders) + 1:03d}"


# -----------------------------
# Catalog Filter & Order Logic
# -----------------------------
def filter_products(
    query: Optional[str] = None,
    max_price: Optional[int] = None,
    category: Optional[str] = None,
    color: Optional[str] = None,
) -> List[Dict[str, Any]]:
    products = load_catalog()
    results: List[Dict[str, Any]] = []

    q_lower = query.lower() if query else None
    cat_lower = category.lower() if category else None
    color_lower = color.lower() if color else None

    for p in products:
        if cat_lower and p.get("category", "").lower() != cat_lower:
            continue
        if color_lower and p.get("color", "").lower() != color_lower:
            continue
        if max_price is not None and p.get("price", 0) > max_price:
            continue
        if q_lower:
            blob = (p.get("name", "") + " " + p.get("description", "")).lower()
            if q_lower not in blob:
                tags = " ".join(p.get("tags", [])).lower()
                if q_lower not in tags:
                    continue
        results.append(p)
    return results


def compute_cart_total(cart_items: List[Dict[str, Any]]) -> int:
    return sum(int(it["unit_price"]) * int(it["quantity"]) for it in cart_items)


# -----------------------------
# Runtime State
# -----------------------------
@dataclass
class CommerceState:
    last_results: List[Dict[str, Any]] = field(default_factory=list)
    cart_items: List[Dict[str, Any]] = field(default_factory=list)
    last_order_id: Optional[str] = None


@dataclass
class Userdata:
    commerce: CommerceState
    agent_session: Optional[AgentSession] = None


# -----------------------------
# Tools
# -----------------------------
@function_tool
async def list_products(
    ctx: RunContext[Userdata],
    query: Annotated[
        Optional[str],
        Field(description="Search keywords like 'black hoodie' or 'coffee mug'.", default=None)
    ] = None,

    max_price: Annotated[
        Optional[int],
        Field(description="Maximum price in INR.", default=None)
    ] = None,

    category: Annotated[
        Optional[str],
        Field(description="Category: hoodie, mug, tshirt, accessory.", default=None)
    ] = None,

    color: Annotated[
        Optional[str],
        Field(description="Color preference like black, white, navy.", default=None)
    ] = None,
) -> str:


    """
    Filter the product catalog and return a natural language summary.
    Also updates 'last_results' in the commerce state.
    """
    state = ctx.userdata.commerce
    results = filter_products(query=query, max_price=max_price, category=category, color=color)

    state.last_results = results

    if not results:
        return "I couldn't find any products matching that description. You can try a different color, category, or budget."

    lines = []
    for idx, p in enumerate(results[:5], start=1):
        lines.append(
            f"{idx}. {p['name']} — {p['price']} {p.get('currency', CURRENCY)} "
            f"({p.get('color', 'color not specified')}, category: {p.get('category', 'other')})"
        )

    summary = "Here are a few options I found:\n" + "\n".join(lines)
    summary += "\n\nYou can say things like 'Add the second one to my cart' or 'Add two of the first hoodies'."
    return summary


@function_tool
async def add_to_cart_from_results(
    ctx: RunContext[Userdata],
    item_index: Annotated[int, Field(description="1-based index from the last product search results.")],
    quantity: Annotated[int, Field(description="Quantity to add.")] = 1,
) -> str:
    """
    Add an item to the cart based on index from last_results.
    """
    state = ctx.userdata.commerce
    results = state.last_results

    if not results:
        return "I don't have any recent product list to refer to. First ask me to show you some products."

    if item_index < 1 or item_index > len(results):
        return f"That item number is out of range. Please choose a number between 1 and {len(results)}."

    product = results[item_index - 1]
    qty = max(1, quantity)

    # see if already in cart
    existing = None
    for it in state.cart_items:
        if it["product_id"] == product["id"]:
            existing = it
            break

    if existing:
        existing["quantity"] += qty
    else:
        state.cart_items.append(
            {
                "product_id": product["id"],
                "name": product["name"],
                "quantity": qty,
                "unit_price": int(product["price"]),
                "currency": product.get("currency", CURRENCY),
            }
        )

    total = compute_cart_total(state.cart_items)
    return (
        f"Added {qty} × {product['name']} to your cart. "
        f"Your current cart total is {total} {CURRENCY}."
    )


@function_tool
async def remove_from_cart(
    ctx: RunContext[Userdata],
    cart_index: Annotated[int, Field(description="1-based index of the item in the current cart list.")],
) -> str:
    """
    Remove an item from the cart by index.
    """
    state = ctx.userdata.commerce
    if not state.cart_items:
        return "Your cart is currently empty."

    if cart_index < 1 or cart_index > len(state.cart_items):
        return f"That cart item number is out of range. Please choose between 1 and {len(state.cart_items)}."

    removed = state.cart_items.pop(cart_index - 1)
    total = compute_cart_total(state.cart_items)
    msg = f"Removed {removed['name']} from your cart."
    if state.cart_items:
        msg += f" Your new cart total is {total} {CURRENCY}."
    else:
        msg += " Your cart is now empty."
    return msg


@function_tool
async def show_cart(ctx: RunContext[Userdata]) -> str:
    """
    Summarize the current cart contents and total amount.
    """
    state = ctx.userdata.commerce
    if not state.cart_items:
        return "Your cart is empty right now."

    lines = []
    for idx, it in enumerate(state.cart_items, start=1):
        lines.append(
            f"{idx}. {it['quantity']} × {it['name']} — {it['unit_price']} {it['currency']} each"
        )

    total = compute_cart_total(state.cart_items)
    summary = "Here is your current cart:\n" + "\n".join(lines)
    summary += f"\n\nCart total: {total} {CURRENCY}."
    summary += " You can remove an item by saying something like 'Remove the second item from my cart'."
    return summary


@function_tool
async def checkout_cart(
    ctx: RunContext[Userdata],
    buyer_name: Annotated[
        Optional[str],
        Field(description="Optional buyer name to attach to the demo order."),
    ] = None,
) -> str:
    """
    Convert the current cart into an order, save it, and clear the cart.
    """
    state = ctx.userdata.commerce
    if not state.cart_items:
        return "Your cart is empty. Add at least one item before checking out."

    items = []
    total = 0
    for it in state.cart_items:
        qty = int(it["quantity"])
        unit = int(it["unit_price"])
        line_total = qty * unit
        total += line_total
        items.append(
            {
                "product_id": it["product_id"],
                "name": it["name"],
                "quantity": qty,
                "unit_amount": unit,
                "currency": it.get("currency", CURRENCY),
                "line_total": line_total,
            }
        )

    order = {
        "id": generate_order_id(),
        "items": items,
        "currency": CURRENCY,
        "total": total,
        "buyer": {"name": buyer_name or "Guest"},
        "status": "PENDING",
        "created_at": datetime.utcnow().isoformat() + "Z",
    }

    orders = load_orders()
    orders.append(order)
    save_orders(orders)

    state.last_order_id = order["id"]
    state.cart_items.clear()

    desc = ", ".join(f"{it['quantity']} × {it['name']}" for it in order["items"])
    return (
        f"Your order {order['id']} has been created for {desc}, with a total of {order['total']} {order['currency']}. "
        "This is a demo order only—no real payment is processed. Your cart is now empty."
    )


@function_tool
async def get_last_order_summary(ctx: RunContext[Userdata]) -> str:
    """
    Return a short summary of the most recent order.
    """
    state = ctx.userdata.commerce
    orders = load_orders()

    last = None
    if state.last_order_id:
        for o in orders:
            if o["id"] == state.last_order_id:
                last = o
                break

    if not last and orders:
        last = orders[-1]

    if not last:
        return "You haven't placed any orders yet in this demo."

    items_desc = ", ".join(f"{it['quantity']} × {it['name']}" for it in last["items"])
    return (
        f"Your most recent order is {last['id']} for {items_desc}, "
        f"totaling {last['total']} {last['currency']}. Status is {last.get('status', 'PENDING')}."
    )


# -----------------------------
# Agent Definition
# -----------------------------
class EcommerceCartAgent(Agent):
    def __init__(self):
        instructions = f"""
You are a friendly voice-based shopping assistant for {BRAND_NAME}.

GOAL:
- Help the user browse a small catalog (mugs, t-shirts, hoodies, accessories).
- Let them add items to a cart, review the cart, and then check out.
- Always use the tools instead of inventing products or prices.

BROWSING:
- When the user asks things like:
  - "Show me black hoodies under 1600"
  - "Any coffee mugs around 400 rupees?"
  - "Do you have developer t-shirts?"
- Call list_products with an appropriate query, max_price, category, or color.
- Then read back the top results with index numbers (1, 2, 3, ...).

CART:
- When the user says:
  - "Add the second one to my cart"
  - "Add two of the first hoodies"
- Interpret the reference as an index into the latest list_products results.
- Call add_to_cart_from_results with that index and quantity.
- Confirm what was added and the updated cart total.

- When they ask:
  - "What's in my cart?"
- Call show_cart and read the summary.

- When they say:
  - "Remove the second item from my cart"
- Call remove_from_cart with that index.

CHECKOUT:
- When the user says:
  - "Checkout", "Place my order", or "I'm done, place the order"
- First call show_cart to confirm items if needed.
- Then call checkout_cart, optionally passing their name if they mention it.
- After checkout, the cart should be empty.

ORDER HISTORY:
- If they ask:
  - "What did I just buy?" or "What was my last order?"
- Call get_last_order_summary and read it out.

STYLE:
- Be concise, polite, and structured.
- Never claim to charge real money: explicitly say it's a demo / sandbox order.
- Keep the conversation focused on discovering products, managing the cart, and placing demo orders.
"""
        super().__init__(
            instructions=instructions,
            tools=[
                list_products,
                add_to_cart_from_results,
                remove_from_cart,
                show_cart,
                checkout_cart,
                get_last_order_summary,
            ],
        )


# -----------------------------
# Prewarm & Entrypoint
# -----------------------------
def prewarm(proc: JobProcess):
    ensure_data_files()
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name}
    print("Starting Day 9 – Zepto E-commerce Cart Agent")

    commerce_state = CommerceState()
    userdata = Userdata(commerce=commerce_state)

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            model="en-US-falcon",
            api_key=os.environ.get("MURF_API_KEY", ""),
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        userdata=userdata,
    )

    userdata.agent_session = session

    await session.start(
        agent=EcommerceCartAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
