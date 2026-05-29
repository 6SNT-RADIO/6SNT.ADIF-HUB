import { useEffect, useRef, useState, type MutableRefObject } from "react";
import { Icon } from "./Icon";
import { useI18n } from "../i18n";

type Props = {
  disabled: boolean;
  onUpload: (files: File[]) => void;
  // Lets external triggers (e.g. NEW_LOG_IMPORT) open the file picker.
  openRef?: MutableRefObject<(() => void) | null>;
};

const formats = ["ADI", "ADX", "CBR", "CSV", "XLSX", "JSON"];

export function DropZone({ disabled, onUpload, openRef }: Props) {
  const { t } = useI18n();
  const inputRef = useRef<HTMLInputElement>(null);
  const [active, setActive] = useState(false);

  useEffect(() => {
    if (!openRef) return;
    openRef.current = () => inputRef.current?.click();
    return () => {
      openRef.current = null;
    };
  }, [openRef]);

  function submit(files: FileList | null) {
    const list = Array.from(files ?? []);
    if (list.length > 0 && !disabled) onUpload(list);
  }

  return (
    <button
      type="button"
      disabled={disabled}
      onClick={() => inputRef.current?.click()}
      onDragOver={(event) => {
        event.preventDefault();
        setActive(true);
      }}
      onDragLeave={() => setActive(false)}
      onDrop={(event) => {
        event.preventDefault();
        setActive(false);
        submit(event.dataTransfer.files);
      }}
      className={`group recessed-well flex h-full min-h-[320px] w-full flex-col items-center justify-center border-2 border-dashed p-12 text-center transition-colors duration-500 ${
        active ? "border-tertiary-fixed bg-[rgba(255,186,56,0.05)]" : "border-tertiary-fixed-dim/30 hover:border-tertiary-fixed"
      } ${disabled ? "cursor-wait opacity-70" : "cursor-crosshair"}`}
    >
      <input
        ref={inputRef}
        className="hidden"
        type="file"
        multiple
        accept=".adi,.adif,.adx,.cbr,.log,.csv,.tsv,.xlsx,.json"
        onChange={(event) => submit(event.currentTarget.files)}
      />
      <Icon
        name="cloud_upload"
        className="mb-4 text-6xl text-tertiary-fixed-dim transition-transform group-hover:scale-110"
      />
      <h2 className="mb-2 text-headline-md uppercase text-primary">{t("dropZone.headline")}</h2>
      <p className="mb-8 max-w-md text-body-md text-on-surface-variant">
        {t("dropZone.description")}
      </p>
      <div className="flex flex-wrap justify-center gap-4">
        {formats.map((code) => (
          <div key={code} className="flex flex-col items-center gap-1 opacity-50 transition-opacity hover:opacity-100">
            <div className="hardware-gradient flex h-12 w-12 items-center justify-center border border-outline-variant text-xs font-bold">
              {code}
            </div>
            <span className="text-label-micro">{t(`dropZone.formats.${code}`)}</span>
          </div>
        ))}
      </div>
    </button>
  );
}
