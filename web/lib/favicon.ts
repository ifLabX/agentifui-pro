const DATA_ATTRIBUTE = "data-branding-managed";

export type FaviconLinks = {
  favicon?: string;
  appleTouchIcon?: string;
  manifest?: string;
};

const removeManagedLinks = () => {
  if (typeof document === "undefined") return;
  document
    .querySelectorAll<HTMLLinkElement>(`link[${DATA_ATTRIBUTE}="true"]`)
    .forEach(link => {
      link.parentElement?.removeChild(link);
    });
};

const createLink = (rel: string, href: string) => {
  const link = document.createElement("link");
  link.rel = rel;
  link.href = href;
  link.setAttribute(DATA_ATTRIBUTE, "true");
  return link;
};

export const setFaviconLinks = ({
  favicon,
  appleTouchIcon,
  manifest,
}: FaviconLinks) => {
  if (typeof document === "undefined") return;

  removeManagedLinks();

  const fragment = document.createDocumentFragment();

  if (favicon) {
    fragment.appendChild(createLink("icon", favicon));
    fragment.appendChild(createLink("shortcut icon", favicon));
  }

  if (appleTouchIcon) {
    fragment.appendChild(createLink("apple-touch-icon", appleTouchIcon));
  }

  if (manifest) {
    fragment.appendChild(createLink("manifest", manifest));
  }

  if (fragment.childNodes.length > 0) {
    document.head.appendChild(fragment);
  }
};
