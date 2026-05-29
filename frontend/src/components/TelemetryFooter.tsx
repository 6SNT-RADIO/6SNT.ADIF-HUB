import type { ImportBatch } from "../lib/types";
import { useI18n } from "../i18n";

type Props = {
  batch: ImportBatch;
};

export function TelemetryFooter({ batch }: Props) {
  const { t } = useI18n();
  const total = batch.normalized_records || batch.total_records;
  const distinctCalls = new Set(batch.qsos.map((qso) => qso.call).filter(Boolean)).size;
  const uniqueCalls = distinctCalls > 0 ? distinctCalls : Math.max(total - batch.duplicate_records, 0);
  return (
    <footer className="fixed bottom-0 z-50 flex h-footer-h w-full items-center justify-between border-t border-outline-variant bg-surface-well px-4">
      <div className="flex items-center gap-6">
        <span className="text-label-micro text-on-surface-variant">{t("footer.ready")}</span>
        <div className="flex items-center gap-2">
          <div className="h-2 w-2 animate-pulse rounded-full bg-primary-fixed-dim shadow-emerald-led" />
          <span className="text-telemetry uppercase text-primary-fixed-dim">{t("footer.flow")}</span>
        </div>
      </div>
      <div className="flex items-center gap-6 text-telemetry uppercase text-tertiary-fixed-dim">
        <span className="cursor-default transition-colors hover:text-primary">{t("footer.total")}: {total.toLocaleString()}</span>
        <span className="cursor-default transition-colors hover:text-primary">{t("footer.calls")}: {uniqueCalls.toLocaleString()}</span>
        <span className="cursor-default transition-colors hover:text-primary">{t("footer.duplicates")}: {batch.duplicate_records.toLocaleString()}</span>
      </div>
    </footer>
  );
}
