export type SourceFile = {
  id: string;
  filename: string;
  format: string;
  status: string;
  record_count: number;
  columns: string[];
  automap: Record<string, string>;
  warnings: string[];
  preview: Record<string, string>[];
};

export type NormalizedQso = {
  id: string;
  status: string;
  call?: string;
  qso_date?: string;
  time_on?: string;
  band?: string;
  freq?: string;
  mode?: string;
  record: Record<string, string>;
};

export type ConflictSummary = {
  call: string | null;
  band: string | null;
  mode: string | null;
  qso_date: string | null;
  time_on: string | null;
};

export type Conflict = {
  id: string;
  reason: string;
  status: string;
  fields: Record<string, { incoming: string; existing: string }>;
  summary?: ConflictSummary;
};

export type ResolveStrategy = "merge" | "use_existing" | "use_incoming" | "use_newer" | "manual";

export type ImportBatch = {
  id: string;
  status: string;
  created_at: string;
  source_count: number;
  total_records: number;
  normalized_records: number;
  duplicate_records: number;
  conflict_records: number;
  export_path?: string;
  sources: SourceFile[];
  qsos: NormalizedQso[];
  conflicts: Conflict[];
  adif_version: string;
  field_options: string[];
};

export type InferenceState = {
  infer_band_from_freq: boolean;
  maidenhead_geoconversion: boolean;
  state_from_exchange: boolean;
};

