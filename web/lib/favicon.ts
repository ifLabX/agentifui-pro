const DATA_ATTRIBUTE = "data-branding-managed";

export type FaviconLinks = {
  favicon?: string;
  appleTouchIcon?: string;
  manifest?: string;
};

const removeManagedLinksByRel = (rel: string) => {
  if (typeof document === "undefined") return;
  document
    .querySelectorAll<HTMLLinkElement>(
      `link[rel='${rel}'][${DATA_ATTRIBUTE}="true"]`
    )
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

const upsertManagedLink = (rel: string, href: string) => {
  if (typeof document === "undefined") return;
  const existing = document.querySelector<HTMLLinkElement>(
    `link[rel='${rel}'][${DATA_ATTRIBUTE}="true"]`
  );
  if (existing) {
    existing.href = href;
    return;
  }
  const link = createLink(rel, href);
  if (document.head.firstChild) {
    document.head.insertBefore(link, document.head.firstChild);
  } else {
    document.head.appendChild(link);
  }
};

export const setFaviconLinks = ({
  favicon,
  appleTouchIcon,
  manifest,
}: FaviconLinks) => {
  if (typeof document === "undefined") return;

  if (favicon) {
    upsertManagedLink("icon", favicon);
    upsertManagedLink("shortcut icon", favicon);
  } else {
    removeManagedLinksByRel("icon");
    removeManagedLinksByRel("shortcut icon");
  }

  if (appleTouchIcon) {
    upsertManagedLink("apple-touch-icon", appleTouchIcon);
  } else {
    removeManagedLinksByRel("apple-touch-icon");
  }

  if (manifest) {
    upsertManagedLink("manifest", manifest);
  } else {
    removeManagedLinksByRel("manifest");
  }
};
