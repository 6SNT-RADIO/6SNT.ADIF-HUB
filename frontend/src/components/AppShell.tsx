import { useRef, useState } from "react";
import type { ImportBatch, InferenceState, ResolveStrategy } from "../lib/types";
import { useI18n } from "../i18n";
import { ColumnMapper } from "./ColumnMapper";
import { ConflictReview } from "./ConflictReview";
import { DropZone } from "./DropZone";
import { ExportPanel } from "./ExportPanel";
import { IngestQueue } from "./IngestQueue";
import { Icon } from "./Icon";
import { QsoPreviewTable } from "./QsoPreviewTable";
import { SemanticInferencePanel } from "./SemanticInferencePanel";
import { SideNav } from "./SideNav";
import { TelemetryFooter } from "./TelemetryFooter";
import { TopNav } from "./TopNav";

type Props = {
  batch: ImportBatch;
  busy: boolean;
  error: string | null;
  mapping: Record<string, string>;
  inference: InferenceState;
  onUpload: (files: File[]) => void;
  onMappingChange: (column: string, field: string) => void;
  onInferenceChange: (key: keyof InferenceState, value: boolean) => void;
  onNormalize: () => void;
  onDedupe: () => void;
  onResolve: (conflictId: string, strategy: ResolveStrategy, fieldChoices: Record<string, "incoming" | "existing">) => void;
};

// Aviso reutilizable cuando una etapa todavía no tiene datos.
function EmptyHint({ icon, text }: { icon: string; text: string }) {
  return (
    <section className="col-span-12 flex flex-col items-center gap-3 bg-surface-panel p-12 text-center">
      <Icon name={icon} className="text-4xl text-label-muted" />
      <p className="text-label-caps uppercase text-on-surface-variant opacity-70">{text}</p>
    </section>
  );
}

export function AppShell({
  batch,
  busy,
  error,
  mapping,
  inference,
  onUpload,
  onMappingChange,
  onInferenceChange,
  onNormalize,
  onDedupe,
  onResolve,
}: Props) {
  const { t } = useI18n();
  const openPicker = useRef<(() => void) | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);
  const [section, setSection] = useState("INGEST");
  const [query, setQuery] = useState("");
  const selectedSource = batch.sources.find((source) => source.status.includes("mapper")) ?? batch.sources[batch.sources.length - 1];
  const status = busy ? t("status.parsing") : t(`status.${batch.status}`);
  const hasNormalized = batch.normalized_records > 0;

  function newImport() {
    setSection("INGEST");
    fileInput.current?.click();
  }

  return (
    <div className="flex h-screen flex-col overflow-hidden bg-surface-container-lowest text-on-surface">
      <TopNav status={status} query={query} onSearch={setQuery} />
      <input
        ref={fileInput}
        className="hidden"
        type="file"
        multiple
        accept=".adi,.adif,.adx,.cbr,.log,.csv,.tsv,.xlsx,.json"
        onChange={(event) => {
          const list = Array.from(event.currentTarget.files ?? []);
          if (list.length > 0) onUpload(list);
          event.currentTarget.value = "";
        }}
      />
      <div className="flex min-h-0 flex-1 overflow-hidden pb-footer-h">
        <SideNav active={section} onSelect={setSection} onNewImport={newImport} />
        <main className="flex min-h-0 flex-1 flex-col gap-px overflow-y-auto bg-surface-container-lowest">
          <section className="flex items-end justify-between border-b border-outline-variant bg-surface-panel p-panel-pad">
            <div>
              <h1 className="text-headline-lg font-black uppercase text-primary">{t(`views.${section}.title`)}</h1>
              <p className="text-label-caps uppercase text-on-surface-variant opacity-60">{t(`views.${section}.subtitle`)}</p>
            </div>
            <div className="bg-surface-well border-l-2 border-primary-fixed px-3 py-1">
              <div className="text-label-micro uppercase opacity-50">{t("shell.status")}</div>
              <div className="animate-pulse text-label-caps uppercase text-primary-fixed">{status}</div>
            </div>
          </section>

          {error ? (
            <section className="border-t border-status-red bg-surface-panel p-panel-pad text-label-caps uppercase text-status-red">
              {t("shell.apiError")}: {error}
            </section>
          ) : null}

          <div className="grid flex-1 grid-cols-12 content-start gap-px">
            {section === "INGEST" ? (
              <>
                <section className="col-span-12 bg-surface-panel p-panel-pad lg:col-span-8">
                  <DropZone disabled={busy} onUpload={onUpload} openRef={openPicker} />
                </section>
                <aside className="col-span-12 flex flex-col gap-4 bg-surface-panel p-panel-pad lg:col-span-4">
                  <IngestQueue batch={batch} busy={busy} />
                  <SemanticInferencePanel inference={inference} onChange={onInferenceChange} />
                </aside>
              </>
            ) : null}

            {section === "PROCESS" ? (
              selectedSource ? (
                <>
                  <ColumnMapper
                    source={selectedSource}
                    mapping={mapping}
                    fieldOptions={batch.field_options}
                    busy={busy}
                    onChange={onMappingChange}
                    onNormalize={onNormalize}
                  />
                  <QsoPreviewTable batch={batch} query={query} />
                </>
              ) : (
                <EmptyHint icon="upload_file" text={t("shell.emptyProcess")} />
              )
            ) : null}

            {section === "MERGE" ? (
              hasNormalized ? (
                <ConflictReview
                  conflicts={batch.conflicts}
                  onDedupe={onDedupe}
                  onResolve={onResolve}
                  busy={busy}
                  disabled={busy}
                />
              ) : (
                <EmptyHint icon="query_stats" text={t("shell.emptyMerge")} />
              )
            ) : null}

            {section === "EXPORT" ? (
              hasNormalized ? (
                <ExportPanel batch={batch} />
              ) : (
                <EmptyHint icon="file_download" text={t("shell.emptyExport")} />
              )
            ) : null}
          </div>
        </main>
      </div>
      <TelemetryFooter batch={batch} />
    </div>
  );
}
