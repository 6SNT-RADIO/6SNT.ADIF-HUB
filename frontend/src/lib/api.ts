import type { ImportBatch, InferenceState, ResolveStrategy } from "./types";

async function parseJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || response.statusText);
  }
  return response.json() as Promise<T>;
}

export async function uploadFiles(files: File[]): Promise<ImportBatch> {
  const form = new FormData();
  files.forEach((file) => form.append("files", file));
  return parseJson<ImportBatch>(
    await fetch("/api/imports", {
      method: "POST",
      body: form,
    }),
  );
}

export async function applyMapping(
  batchId: string,
  mapping: Record<string, string>,
  inference: InferenceState,
): Promise<ImportBatch> {
  return parseJson<ImportBatch>(
    await fetch(`/api/imports/${batchId}/mapping`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mapping, inference }),
    }),
  );
}

export async function dedupeBatch(batchId: string): Promise<ImportBatch> {
  return parseJson<ImportBatch>(
    await fetch(`/api/imports/${batchId}/dedupe`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tolerance_minutes: 15 }),
    }),
  );
}

export async function resolveConflict(
  batchId: string,
  conflictId: string,
  strategy: ResolveStrategy,
  fieldChoices: Record<string, "incoming" | "existing"> = {},
): Promise<ImportBatch> {
  return parseJson<ImportBatch>(
    await fetch(`/api/imports/${batchId}/conflicts/${conflictId}/resolve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ strategy, field_choices: fieldChoices }),
    }),
  );
}

export function exportUrl(batchId: string): string {
  return `/api/exports/${batchId}.adi`;
}

