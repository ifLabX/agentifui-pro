export type FormatTitleOptions = {
  title?: string;
  brand?: string;
  suffix?: string;
  separator?: string;
};

const DEFAULT_SEPARATOR = " - ";

export const formatTitle = ({
  title,
  brand,
  suffix,
  separator = DEFAULT_SEPARATOR,
}: FormatTitleOptions): string => {
  const clean = (value?: string) => value?.trim() || "";

  const cleanedTitle = clean(title);
  const cleanedBrand = clean(brand);
  const cleanedSuffix = clean(suffix);

  const hasContent = (value: string) => value.length > 0;

  const titleAndBrand = [cleanedTitle, cleanedBrand]
    .filter(hasContent)
    .join(separator);

  return [titleAndBrand, cleanedSuffix].filter(hasContent).join(" ");
};
