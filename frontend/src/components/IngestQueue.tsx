import type { ImportBatch } from "../lib/types";
import { useI18n } from "../i18n";

type Props = {
  batch: ImportBatch;
  busy: boolean;
};

export function IngestQueue({ batch, busy }: Props) {
  const { t } = useI18n();
  const activeCount = batch.sources.length;
  return (
    <section className="flex flex-col gap-4">
      <div className="flex items-center justify-between border-b border-outline-variant pb-2">
        <span className="text-headline-md uppercase">{t("ingestQueue.title")}</span>
        <span className="bg-secondary-container/20 px-2 text-label-micro text-secondary">
          {activeCount} {activeCount === 1 ? t("ingestQueue.activeSingular") : t("ingestQueue.activePlural")}
        </span>
      </div>
      {activeCount === 0 ? (
        <div className="recessed-well p-4 text-center text-label-caps uppercase text-on-surface-variant opacity-70">
          {t("ingestQueue.empty")}
        </div>
      ) : (
        <div className="flex max-h-56 flex-col gap-px overflow-y-auto bg-outline-variant">
          {batch.sources.map((source, index) => {
            const analyzing = busy && index === 0;
            return (
              <div key={source.id} className="flex flex-col gap-2 bg-surface-well p-3">
                <div className="flex items-start justify-between gap-3">
                  <div className="truncate text-label-caps text-primary" title={source.filename}>
                    {source.filename}
                  </div>
                  <span className="text-label-micro text-secondary">
                    {analyzing ? t("ingestQueue.analyzing") : t(`status.${source.status}`)}
                  </span>
                </div>
                <div className="h-1 w-full overflow-hidden bg-surface-container">
                  <div
                    className={`h-full bg-gradient-to-r from-primary-fixed-dim to-secondary-fixed-dim ${analyzing ? "animate-pulse" : ""}`}
                    style={{ width: analyzing ? "66%" : "100%" }}
                  />
                </div>
                <div className="flex justify-between text-label-micro text-on-surface-variant">
                  <span>
                    {source.record_count.toLocaleString()} {t("ingestQueue.records")} / {source.format}
                  </span>
                  <span>{source.warnings.length > 0 ? t("ingestQueue.review") : t("ingestQueue.ok")}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}
