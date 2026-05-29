import { Icon } from "./Icon";
import { useI18n } from "../i18n";

type Props = {
  active: string;
  onSelect?: (label: string) => void;
  onNewImport?: () => void;
};

const items = [
  { id: "INGEST", icon: "upload_file" },
  { id: "PROCESS", icon: "query_stats" },
  { id: "MERGE", icon: "call_merge" },
  { id: "EXPORT", icon: "file_download" },
];

export function SideNav({ active, onSelect, onNewImport }: Props) {
  const { t } = useI18n();
  return (
    <aside className="flex h-full w-sidebar-w shrink-0 flex-col border-r border-outline-variant bg-surface-container shadow-well">
      <div className="border-b border-outline-variant p-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center border border-outline-variant bg-surface-well">
            <Icon name="hub" className="text-secondary" />
          </div>
          <div>
            <div className="text-headline-md text-on-surface">{t("sideNav.processor")}</div>
            <div className="text-label-micro text-secondary">{t("sideNav.adifLocal")}</div>
          </div>
        </div>
      </div>
      <nav className="flex flex-1 flex-col gap-1 py-4">
        {items.map(({ id, icon }) => {
          const selected = id === active;
          return (
            <button
              key={id}
              onClick={() => onSelect?.(id)}
              className={`flex items-center gap-4 px-4 py-3 text-left text-label-caps transition-all ${
                selected
                  ? "scale-95 border-l-4 border-secondary bg-surface-well font-bold text-secondary active:scale-90"
                  : "text-on-surface-variant opacity-70 hover:bg-surface-container-high hover:text-primary"
              }`}
            >
              <Icon name={icon} />
              {t(`sideNav.items.${id}`)}
            </button>
          );
        })}
      </nav>
      <div className="mt-auto p-4">
        <button
          onClick={onNewImport}
          className="hardware-gradient w-full border border-outline-variant py-2 text-label-caps text-primary transition-all hover:border-primary"
        >
          {t("sideNav.newImport")}
        </button>
      </div>
    </aside>
  );
}
