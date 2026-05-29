import { Icon } from "./Icon";
import { useI18n, type Locale } from "../i18n";

type Props = {
  status: string;
  query: string;
  onSearch: (query: string) => void;
};

export function TopNav({ status, query, onSearch }: Props) {
  const { locale, setLocale, t } = useI18n();
  const locales: Locale[] = ["es", "en"];

  return (
    <header className="z-50 flex h-header-h w-full items-center justify-between border-b border-outline-variant bg-surface-panel px-4">
      <span className="text-headline-lg font-black text-primary dark:text-primary-fixed">6SNT.ADIF-HUB</span>
      <div className="flex items-center gap-4">
        <div className="recessed-well flex h-8 items-center gap-2 px-3">
          <Icon name="search" className="text-secondary" title={t("topNav.searchTitle")} />
          <input
            value={query}
            className="w-48 border-none bg-transparent text-label-caps text-on-surface-variant outline-none placeholder:text-on-surface-variant"
            placeholder={t("topNav.searchPlaceholder")}
            onChange={(event) => onSearch(event.currentTarget.value)}
          />
        </div>
        <div className="hidden h-8 items-center border border-outline-variant bg-surface-well md:flex" aria-label={t("language.label")}>
          {locales.map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => setLocale(item)}
              className={`h-full px-3 text-label-micro uppercase transition-colors ${
                item === locale ? "bg-secondary-container/30 text-secondary" : "text-on-surface-variant hover:text-primary"
              }`}
              aria-pressed={item === locale}
              title={t(`language.${item}`)}
            >
              {item.toUpperCase()}
            </button>
          ))}
        </div>
        <span className="hidden text-label-micro uppercase text-label-muted md:block">{status}</span>
      </div>
    </header>
  );
}
