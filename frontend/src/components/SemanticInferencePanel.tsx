import type { InferenceState } from "../lib/types";
import { useI18n } from "../i18n";

type Props = {
  inference: InferenceState;
  onChange: (key: keyof InferenceState, value: boolean) => void;
};

const rows: Array<[keyof InferenceState, string]> = [
  ["infer_band_from_freq", "semanticInference.inferBand"],
  ["maidenhead_geoconversion", "semanticInference.maidenhead"],
  ["state_from_exchange", "semanticInference.state"],
];

export function SemanticInferencePanel({ inference, onChange }: Props) {
  const { t } = useI18n();
  return (
    <section className="mt-2 flex flex-col gap-4 border-t border-outline-variant pt-4">
      <span className="text-headline-md uppercase">{t("semanticInference.title")}</span>
      <div className="flex flex-col gap-3">
        {rows.map(([key, label]) => {
          const enabled = inference[key];
          return (
            <button
              key={key}
              className="group flex cursor-pointer items-center justify-between text-left"
              onClick={() => onChange(key, !enabled)}
            >
              <span className="text-label-caps text-on-surface-variant transition-colors group-hover:text-primary">{t(label)}</span>
              <span className="relative h-4 w-8 border border-outline-variant bg-surface-well">
                <span
                  className={`absolute inset-y-0.5 h-3 w-3 transition-all ${
                    enabled ? "right-0.5 bg-primary-fixed-dim shadow-emerald-led" : "left-0.5 bg-surface-container-highest"
                  }`}
                />
              </span>
            </button>
          );
        })}
      </div>
    </section>
  );
}
