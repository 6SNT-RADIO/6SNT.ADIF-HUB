import { Icon } from "./Icon";
import type { SourceFile } from "../lib/types";
import { useI18n } from "../i18n";

type Props = {
  source: SourceFile;
  mapping: Record<string, string>;
  fieldOptions: string[];
  busy: boolean;
  onChange: (column: string, field: string) => void;
  onNormalize: () => void;
};

export function ColumnMapper({ source, mapping, fieldOptions, busy, onChange, onNormalize }: Props) {
  const { t } = useI18n();
  const columns = source.columns.length > 0 ? source.columns : Object.keys(source.preview[0] ?? {});
  const unmapped = columns.filter((column) => !mapping[column]);
  return (
    <section className="col-span-12 border-t border-outline-variant bg-surface-panel p-panel-pad">
      <div className="mb-4 flex items-center gap-4">
        <Icon name="table_chart" className="text-secondary" />
        <h2 className="text-headline-md uppercase">{t("mapper.title")}: {source.filename}</h2>
        <span
          className={`ml-auto text-label-micro uppercase ${unmapped.length > 0 ? "text-status-red" : "text-primary-fixed-dim"}`}
        >
          {unmapped.length > 0 ? t("mapper.incomplete") : t("mapper.ready")}
        </span>
      </div>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        {columns.slice(0, 12).map((column) => {
          const value = mapping[column] ?? "";
          const missing = value === "";
          return (
            <div
              key={column}
              className={`recessed-well flex min-h-[150px] flex-col gap-3 border-l-2 p-4 ${missing ? "border-status-red" : "border-secondary"}`}
            >
              <div className="flex flex-col">
                <span className="text-label-micro uppercase opacity-50">{t("mapper.column")}</span>
                <span className="truncate text-headline-md text-primary" title={column}>
                  {column}
                </span>
              </div>
              {missing ? (
                <Icon name="warning" className="mx-auto animate-pulse text-status-red" />
              ) : (
                <Icon name="link" className="mx-auto text-secondary" />
              )}
              <label className="flex flex-col">
                <span className="text-label-micro uppercase opacity-50">{t("mapper.field")}</span>
                <div
                  className={`recessed-well mt-1 flex items-center justify-between ${missing ? "border-status-red/50" : ""}`}
                >
                  <select
                    className={`h-9 w-full appearance-none bg-transparent px-3 text-label-caps outline-none ${
                      missing ? "italic text-on-surface-variant" : "text-secondary"
                    }`}
                    value={value}
                    onChange={(event) => onChange(column, event.target.value)}
                  >
                    <option value="">{t("mapper.select")}</option>
                    {fieldOptions.map((field) => (
                      <option key={field} value={field}>
                        {field}
                      </option>
                    ))}
                  </select>
                  <Icon name="arrow_drop_down" className="pointer-events-none mr-1 text-sm" />
                </div>
              </label>
            </div>
          );
        })}
      </div>
      <div className="mt-6 flex justify-end gap-3">
        <button
          disabled={busy}
          onClick={onNormalize}
          className="hardware-gradient h-8 border border-secondary px-6 text-label-caps text-secondary transition-all hover:shadow-cyan-glow disabled:cursor-not-allowed disabled:opacity-40"
        >
          {t("mapper.process")}
        </button>
      </div>
    </section>
  );
}
