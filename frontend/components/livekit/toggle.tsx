'use client';

import * as React from 'react';
import { type VariantProps, cva } from 'class-variance-authority';
import * as TogglePrimitive from '@radix-ui/react-toggle';
import { cn } from '@/lib/utils';

const toggleVariants = cva(
  [
    'inline-flex items-center justify-center gap-2 rounded-full',
    'text-sm font-medium whitespace-nowrap',
    'cursor-pointer outline-none transition-[color,box-shadow,background-color]',
    'hover:bg-blue-500/30 hover:text-yellow-300',
    'disabled:pointer-events-none disabled:opacity-50',
    'data-[state=on]:bg-gradient-to-r data-[state=on]:from-yellow-300 data-[state=on]:to-yellow-400 data-[state=on]:text-blue-950 data-[state=on]:font-bold',
    'focus-visible:ring-ring/50 focus-visible:ring-[3px] focus-visible:border-ring',
    'aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive ',
    "[&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 [&_svg]:shrink-0",
  ],
  {
    variants: {
      variant: {
        default: 'bg-transparent text-blue-100',
        primary:
          'bg-blue-500/20 text-yellow-300 data-[state=on]:bg-gradient-to-r data-[state=on]:from-yellow-300 data-[state=on]:to-yellow-400 hover:text-yellow-200 hover:bg-blue-500/40',
        secondary:
          'bg-blue-500/20 border border-blue-500/30 text-blue-100 data-[state=on]:bg-gradient-to-r data-[state=on]:from-yellow-300 data-[state=on]:to-yellow-400 data-[state=on]:text-blue-950 data-[state=on]:border-yellow-400 hover:bg-blue-500/30 hover:border-yellow-400/60',
        outline:
          'border border-blue-500/30 bg-transparent text-blue-100 shadow-xs hover:bg-blue-500/20 hover:text-yellow-300 hover:border-yellow-400/60',
      },
      size: {
        default: 'h-9 px-4 py-2 has-[>svg]:px-3',
        sm: 'h-8 gap-1.5 px-3 has-[>svg]:px-2.5',
        lg: 'h-10 px-6 has-[>svg]:px-4',
        icon: 'size-9',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

function Toggle({
  className,
  variant,
  size,
  ...props
}: React.ComponentProps<typeof TogglePrimitive.Root> & VariantProps<typeof toggleVariants>) {
  return (
    <TogglePrimitive.Root
      data-slot="toggle"
      className={cn(toggleVariants({ variant, size, className }))}
      {...props}
    />
  );
}

export { Toggle, toggleVariants };
