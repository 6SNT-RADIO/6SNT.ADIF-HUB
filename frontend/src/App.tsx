import { useMemo, useState } from "react";
import { applyMapping, dedupeBatch, resolveConflict, uploadFiles } from "./lib/api";
import type { ImportBatch, InferenceState, ResolveStrategy } from "./lib/types";
import { AppShell } from "./components/AppShell";
import { useI18n } from "./i18n";

const DEFAULT_FIELD_OPTIONS = [
  "CALL",
  "STATION_CALLSIGN",
  "QSO_DATE",
  "TIME_ON",
  "BAND",
  "FREQ",
  "MODE",
  "SUBMODE",
  "RST_SENT",
  "RST_RCVD",
  "GRIDSQUARE",
  "STATE",
  "CONTEST_ID",
  "MY_POTA_REF",
  "POTA_REF",
  "COMMENT",
];

// Estado inicial real y vacío: sin lotes ni cifras de demo.
const emptyBatch: ImportBatch = {
  id: "",
  status: "idle",
  created_at: new Date().toISOString(),
  source_count: 0,
  total_records: 0,
  normalized_records: 0,
  duplicate_records: 0,
  conflict_records: 0,
  adif_version: "3.1.7",
  field_options: DEFAULT_FIELD_OPTIONS,
  sources: [],
  qsos: [],
  conflicts: [],
};

export function App() {
  const { t } = useI18n();
  const [batch, setBatch] = useState<ImportBatch>(emptyBatch);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mapping, setMapping] = useState<Record<string, string>>({});
  const [inference, setInference] = useState<InferenceState>({
    infer_band_from_freq: true,
    maidenhead_geoconversion: true,
    state_from_exchange: false,
  });

  const hasBatch = batch.id !== "";

  const effectiveMapping = useMemo(() => {
    const merged: Record<string, string> = {};
    batch.sources.forEach((source) => Object.assign(merged, source.automap));
    Object.assign(merged, mapping);
    return merged;
  }, [batch.sources, mapping]);

  async function run<T>(action: () => Promise<T>, onDone: (result: T) => void) {
    setBusy(true);
    setError(null);
    try {
      onDone(await action());
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : t("app.errorUnknown"));
    } finally {
      setBusy(false);
    }
  }

  function handleUpload(files: File[]) {
    void run(() => uploadFiles(files), (next) => {
      setBatch(next);
      setMapping({});
    });
  }

  function handleNormalize() {
    if (!hasBatch) return;
    void run(() => applyMapping(batch.id, effectiveMapping, inference), setBatch);
  }

  function handleDedupe() {
    if (!hasBatch) return;
    void run(() => dedupeBatch(batch.id), setBatch);
  }

  function handleResolve(
    conflictId: string,
    strategy: ResolveStrategy,
    fieldChoices: Record<string, "incoming" | "existing">,
  ) {
    if (!hasBatch) return;
    void run(() => resolveConflict(batch.id, conflictId, strategy, fieldChoices), setBatch);
  }

  return (
    <AppShell
      batch={batch}
      busy={busy}
      error={error}
      mapping={effectiveMapping}
      inference={inference}
      onUpload={handleUpload}
      onMappingChange={(column, field) => setMapping((current) => ({ ...current, [column]: field }))}
      onInferenceChange={(key, value) => setInference((current) => ({ ...current, [key]: value }))}
      onNormalize={handleNormalize}
      onDedupe={handleDedupe}
      onResolve={handleResolve}
    />
  );
}
