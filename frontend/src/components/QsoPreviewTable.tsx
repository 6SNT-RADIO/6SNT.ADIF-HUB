import type { ImportBatch } from "../lib/types";
import { useI18n } from "../i18n";

type Props = {
  batch: ImportBatch;
  query?: string;
  anchorId?: string;
};

export function QsoPreviewTable({ batch, query = "", anchorId }: Props) {
  const { t } = useI18n();
  const needle = query.trim().toLowerCase();
  const rows = needle
    ? batch.qsos.filter((qso) =>
        [qso.call, qso.qso_date, qso.time_on, qso.band, qso.freq, qso.mode, qso.status]
          .filter(Boolean)
          .some((value) => String(value).toLowerCase().includes(needle)),
      )
    : batch.qsos;
  return (
    <section id={anchorId} className="col-span-12 border-t border-outline-variant bg-surface-panel p-panel-pad">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-headline-md uppercase">{t("preview.title")}</h2>
        <span className="text-label-micro text-on-surface-variant">
          {needle ? `${rows.length} / ` : ""}
          {batch.normalized_records.toLocaleString()} {t("preview.normalized")}
        </span>
      </div>
      <div className="recessed-well max-h-[55vh] overflow-auto">
        <table className="w-full min-w-[780px] border-collapse text-left text-body-md">
          <thead className="sticky top-0 z-10 border-b border-outline-variant bg-surface-well text-label-micro uppercase text-label-muted">
            <tr>
              {[
                t("preview.headers.status"),
                t("preview.headers.call"),
                t("preview.headers.date"),
                t("preview.headers.time"),
                t("preview.headers.band"),
                t("preview.headers.freq"),
                t("preview.headers.mode"),
              ].map((header) => (
                <th key={header} className="px-3 py-2 font-bold">
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr>
                <td className="px-3 py-4 text-label-caps uppercase text-on-surface-variant" colSpan={7}>
                  {needle
                    ? t("preview.noMatches", { query: query.trim().toUpperCase() })
                    : t("preview.empty")}
                </td>
              </tr>
            ) : (
              rows.slice(0, 100).map((row) => (
                <tr key={row.id} className="border-b border-border-subtle last:border-b-0">
                  <td className={row.status === "conflict" ? "px-3 py-2 text-status-red" : "px-3 py-2 text-primary-fixed-dim"}>{t(`status.${row.status}`)}</td>
                  <td className="px-3 py-2 text-primary">{row.call ?? "-"}</td>
                  <td className="px-3 py-2 text-on-surface-variant">{row.qso_date ?? "-"}</td>
                  <td className="px-3 py-2 text-on-surface-variant">{row.time_on ?? "-"}</td>
                  <td className="px-3 py-2 text-secondary">{row.band ?? "-"}</td>
                  <td className="px-3 py-2 text-on-surface-variant">{row.freq ?? "-"}</td>
                  <td className="px-3 py-2 text-on-surface-variant">{row.mode ?? "-"}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
