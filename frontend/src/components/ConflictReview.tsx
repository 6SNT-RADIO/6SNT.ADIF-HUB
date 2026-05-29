import { useState } from "react";
import { Icon } from "./Icon";
import type { Conflict, ResolveStrategy } from "../lib/types";
import { useI18n } from "../i18n";

type Props = {
  conflicts: Conflict[];
  disabled: boolean;
  busy: boolean;
  anchorId?: string;
  onDedupe: () => void;
  onResolve: (conflictId: string, strategy: ResolveStrategy, fieldChoices: Record<string, "incoming" | "existing">) => void;
};

const STRATEGIES: ResolveStrategy[] = ["use_existing", "use_incoming", "merge", "use_newer"];

function summaryLine(conflict: Conflict): string {
  const s = conflict.summary;
  if (!s) return "";
  return [s.call, s.band, s.mode, s.qso_date, s.time_on].filter(Boolean).join(" · ");
}

function ConflictCard({
  conflict,
  busy,
  onResolve,
}: {
  conflict: Conflict;
  busy: boolean;
  onResolve: Props["onResolve"];
}) {
  const { t } = useI18n();
  const fields = Object.entries(conflict.fields);
  // Seleccion por campo (estilo merge de codigo); por defecto se conserva el existente.
  const [choices, setChoices] = useState<Record<string, "incoming" | "existing">>(
    () => Object.fromEntries(fields.map(([field]) => [field, "existing" as const])),
  );
  const resolved = conflict.status === "resolved";

  const cell = (field: string, side: "incoming" | "existing", value: string) => {
    const active = choices[field] === side;
    return (
      <button
        type="button"
        disabled={resolved || busy}
        onClick={() => setChoices((c) => ({ ...c, [field]: side }))}
        className={`truncate px-2 py-1 text-left transition-colors ${
          active
            ? side === "incoming"
              ? "bg-secondary-container/30 text-secondary"
              : "bg-primary-fixed-dim/20 text-primary-fixed-dim"
            : "text-on-surface-variant hover:text-primary"
        }`}
        title={value || t("conflicts.emptyValue")}
      >
        {value || "—"}
      </button>
    );
  };

  return (
    <div className={`recessed-well border-l-2 p-3 ${resolved ? "border-primary-fixed-dim opacity-70" : "border-status-red"}`}>
      <div className="mb-2 flex items-center justify-between gap-2 text-label-caps uppercase">
        <span className="truncate text-primary" title={summaryLine(conflict)}>
          {summaryLine(conflict) || conflict.reason}
        </span>
        <span className={resolved ? "text-primary-fixed-dim" : "text-status-red"}>
          {resolved ? t("conflicts.resolved") : t("conflicts.open")}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-px bg-outline-variant text-label-micro">
        <div className="bg-surface-well px-2 py-1 text-label-muted">{t("conflicts.field")}</div>
        <div className="bg-surface-well px-2 py-1 text-secondary">{t("conflicts.incoming")}</div>
        <div className="bg-surface-well px-2 py-1 text-primary-fixed-dim">{t("conflicts.existing")}</div>
        {fields.slice(0, 8).map(([field, values]) => (
          <div key={field} className="contents">
            <div className="bg-surface-well px-2 py-1 text-on-surface-variant">{field}</div>
            <div className="bg-surface-well">{cell(field, "incoming", values.incoming)}</div>
            <div className="bg-surface-well">{cell(field, "existing", values.existing)}</div>
          </div>
        ))}
      </div>

      {resolved ? null : (
        <>
          <div className="mt-3 flex flex-wrap gap-2">
            {STRATEGIES.map((strategy) => (
              <button
                key={strategy}
                disabled={busy}
                onClick={() => onResolve(conflict.id, strategy, {})}
                className="h-7 border border-outline-variant px-3 text-label-micro uppercase text-on-surface-variant transition-all hover:border-secondary hover:text-secondary disabled:opacity-40"
              >
                {t(`conflicts.strategies.${strategy}`)}
              </button>
            ))}
          </div>
          <div className="mt-2 flex justify-end">
            <button
              disabled={busy}
              onClick={() => onResolve(conflict.id, "manual", choices)}
              className="hardware-gradient h-7 border border-primary-fixed-dim px-4 text-label-micro uppercase text-primary-fixed-dim transition-all hover:shadow-emerald-led disabled:opacity-40"
            >
              {t("conflicts.resolveSelection")}
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export function ConflictReview({ conflicts, disabled, busy, anchorId, onDedupe, onResolve }: Props) {
  const { t } = useI18n();
  const open = conflicts.filter((c) => c.status !== "resolved").length;
  return (
    <section id={anchorId} className="col-span-12 border-t border-outline-variant bg-surface-panel p-panel-pad">
      <div className="mb-3 flex items-center gap-3">
        <Icon name="compare_arrows" className="text-secondary" />
        <h2 className="text-headline-md uppercase">{t("conflicts.title")}</h2>
        {conflicts.length > 0 ? (
          <span className="text-label-micro uppercase text-on-surface-variant">{t("conflicts.openTotal", { open, total: conflicts.length })}</span>
        ) : null}
        <button
          disabled={disabled}
          onClick={onDedupe}
          className="hardware-gradient ml-auto h-8 border border-outline-variant px-4 text-label-caps text-secondary transition-all hover:border-secondary disabled:cursor-not-allowed disabled:opacity-40"
        >
          {t("conflicts.dedupe")}
        </button>
      </div>
      <div className="grid max-h-[60vh] gap-3 overflow-auto md:grid-cols-2">
        {conflicts.length === 0 ? (
          <div className="recessed-well p-3 text-label-caps uppercase text-on-surface-variant">{t("conflicts.noOpen")}</div>
        ) : (
          conflicts.slice(0, 50).map((conflict) => (
            <ConflictCard key={conflict.id} conflict={conflict} busy={busy} onResolve={onResolve} />
          ))
        )}
      </div>
    </section>
  );
}
