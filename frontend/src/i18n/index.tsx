import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import es from "./locales/es.json";
import en from "./locales/en.json";

export type Locale = "es" | "en";

type Messages = typeof es;
type Params = Record<string, string | number>;

const STORAGE_KEY = "6snt.adifhub.locale";
const dictionaries: Record<Locale, Messages> = { es, en };

type I18nContextValue = {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (key: string, params?: Params) => string;
};

const I18nContext = createContext<I18nContextValue | null>(null);

function isLocale(value: string | null): value is Locale {
  return value === "es" || value === "en";
}

function detectInitialLocale(): Locale {
  const stored = typeof window !== "undefined" ? window.localStorage.getItem(STORAGE_KEY) : null;
  if (isLocale(stored)) return stored;

  const browser = typeof navigator !== "undefined" ? navigator.language.toLowerCase() : "";
  if (browser.startsWith("en")) return "en";
  return "es";
}

function readPath(source: unknown, key: string): string | undefined {
  return key.split(".").reduce<unknown>((current, part) => {
    if (current && typeof current === "object" && part in current) {
      return (current as Record<string, unknown>)[part];
    }
    return undefined;
  }, source) as string | undefined;
}

function format(template: string, params: Params = {}): string {
  return Object.entries(params).reduce(
    (output, [name, value]) => output.split(`{${name}}`).join(String(value)),
    template,
  );
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocale] = useState<Locale>(detectInitialLocale);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, locale);
    document.documentElement.lang = locale;
  }, [locale]);

  const value = useMemo<I18nContextValue>(() => {
    function t(key: string, params?: Params): string {
      const text = readPath(dictionaries[locale], key) ?? readPath(dictionaries.es, key) ?? key;
      return format(text, params);
    }

    return { locale, setLocale, t };
  }, [locale]);

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n(): I18nContextValue {
  const context = useContext(I18nContext);
  if (!context) throw new Error("useI18n must be used inside I18nProvider");
  return context;
}
