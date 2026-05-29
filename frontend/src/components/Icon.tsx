type Props = {
  name: string;
  className?: string;
  title?: string;
  filled?: boolean;
};

// Material Symbols Outlined wrapper (local font, no CDN). Brandbook mandates
// this icon set for visibility over the obsidian background.
export function Icon({ name, className = "", title, filled = false }: Props) {
  return (
    <span
      className={`material-symbols-outlined ${className}`}
      style={filled ? { fontVariationSettings: '"FILL" 1, "wght" 400, "GRAD" 0, "opsz" 24' } : undefined}
      title={title}
      aria-hidden={title ? undefined : true}
      role={title ? "img" : undefined}
    >
      {name}
    </span>
  );
}
