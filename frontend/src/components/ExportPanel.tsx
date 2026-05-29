import { Icon } from "./Icon";
import { exportUrl } from "../lib/api";
import type { ImportBatch } from "../lib/types";
import { useI18n } from "../i18n";

type Props = {
  batch: ImportBatch;
  anchorId?: string;
};

export function ExportPanel({ batch, anchorId }: Props) {
  const { t } = useI18n();
  const enabled = batch.id !== "" && batch.normalized_records > 0;
  return (
    <section id={anchorId} className="col-span-12 border-t border-outline-variant bg-surface-panel p-panel-pad">
      <div className="flex items-center gap-4">
        <Icon name="file_download" className="text-secondary" />
        <div>
          <h2 className="text-headline-md uppercase">{t("export.title")}</h2>
          <p className="text-label-micro uppercase text-on-surface-variant">{t("export.subtitle")}</p>
        </div>
        <a
          href={enabled ? exportUrl(batch.id) : undefined}
          className={`hardware-gradient ml-auto border px-6 py-2 text-label-caps transition-all ${
            enabled ? "border-secondary text-secondary hover:shadow-cyan-glow" : "pointer-events-none border-outline-variant text-label-muted opacity-50"
          }`}
        >
          {t("export.download")}
        </a>
      </div>
    </section>
  );
}
