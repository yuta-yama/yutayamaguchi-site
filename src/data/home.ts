/**
 * Homepage content that Yuta can edit without touching layout code.
 *
 * Selected works: change `selectedWorkSlugs` (order is the grid order).
 * Future sections stay off the page until they have real content.
 */

/** Display order for the homepage grid. Slugs match `src/content/projects/`. */
export const selectedWorkSlugs = [
  "maude",
  "wolf",
  "thesecolorsdontrun",
  "until-we-could",
  "jazz-abroad",
  "dell-mike-shinoda",
  "echosmith-cool-kids",
  "mcdonalds-coffee",
];

export const reel = {
  vimeo: "204635110",
  poster: "/stills/dpreel2016/cover.jpg",
  title: "Yuta Yamaguchi reel",
};

export const siteLinks = [
  { href: "https://www.imdb.me/yutayamaguchi", label: "IMDb" },
  { href: "https://www.instagram.com/yutay", label: "Instagram" },
  { href: "https://vimeo.com/yutayamaguchi", label: "Vimeo" },
  { href: "https://www.linkedin.com/in/yuta-yamaguchi-baa2147", label: "LinkedIn" },
  { href: "mailto:yuta.yamaguchi@gmail.com", label: "Email" },
];

export type Highlight = {
  title: string;
  href?: string;
  detail?: string;
};

/** UT and UMAC highlights. Hidden until this list has items. */
export const utUmacHighlights: Highlight[] = [];

export type Note = {
  title: string;
  href?: string;
  date?: string;
  excerpt?: string;
};

/** Notes and writing. Hidden until this list has items. */
export const notes: Note[] = [];

export type SideProject = {
  title: string;
  href?: string;
  summary?: string;
};

/** Side projects. Hidden until this list has items. */
export const sideProjects: SideProject[] = [];

/**
 * Newsletter signup. Hidden until `enabled` is true and `action` is a real endpoint.
 */
export const newsletter = {
  enabled: false,
  heading: "Newsletter",
  blurb: "",
  action: "",
};
