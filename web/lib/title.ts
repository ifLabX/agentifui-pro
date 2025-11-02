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

  let composed = "";

  if (cleanedTitle && cleanedBrand) {
    composed = `${cleanedTitle}${separator}${cleanedBrand}`;
  } else if (cleanedTitle) {
    composed = cleanedTitle;
  } else if (cleanedBrand) {
    composed = cleanedBrand;
  }

  if (cleanedSuffix) {
    composed = composed ? `${composed} ${cleanedSuffix}` : cleanedSuffix;
  }

  return composed;
};
