import * as React from 'react';
import { type VariantProps, cva } from 'class-variance-authority';
import { Slot } from '@radix-ui/react-slot';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  [
    'text-xs font-bold tracking-wider uppercase whitespace-nowrap',
    'inline-flex items-center justify-center gap-2 shrink-0 rounded-full cursor-pointer outline-none transition-colors duration-300',
    'focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]',
    'disabled:pointer-events-none disabled:opacity-50',
    'aria-invalid:ring-destructive/20 aria-invalid:border-destructive dark:aria-invalid:ring-destructive/40 ',
    "[&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 [&_svg]:shrink-0",
  ],
  {
    variants: {
      variant: {
        default: 'bg-blue-500/20 text-blue-100 border border-blue-500/50 hover:bg-blue-500/30 hover:border-yellow-400/60 focus:bg-blue-500/30',
        destructive: [
          'bg-destructive/10 text-destructive',
          'hover:bg-destructive/20 focus:bg-destructive/20 focus-visible:ring-destructive/20',
          'dark:focus-visible:ring-destructive/40',
        ],
        outline: [
          'border border-blue-500/50 bg-blue-900/20',
          'hover:bg-blue-500/20 hover:text-yellow-300 hover:border-yellow-400',
          'dark:bg-blue-900/30 dark:border-blue-500/50 dark:hover:bg-blue-500/30',
        ],
        primary: 'bg-gradient-to-r from-yellow-300 to-yellow-400 text-blue-950 font-bold hover:shadow-lg hover:shadow-yellow-400/50 focus:shadow-lg focus:shadow-yellow-400/50',
        secondary: 'bg-blue-500/20 text-yellow-300 border border-blue-500/30 hover:bg-blue-500/30 hover:border-yellow-400/60',
        ghost: 'hover:bg-blue-500/20 hover:text-yellow-300 dark:hover:bg-blue-500/30',
        link: 'text-yellow-300 underline-offset-4 hover:underline',
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

function Button({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: React.ComponentProps<'button'> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean;
  }) {
  const Comp = asChild ? Slot : 'button';

  return (
    <Comp
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}

export { Button, buttonVariants };
