import { defineCollection, z } from "astro:content";

const projects = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    description: z.string().optional().default(""),
    order: z.number(),
    cover: z.string().optional().default(""),
    stills: z.array(z.string()).default([]),
    vimeo: z.string().optional(),
    youtube: z.string().optional(),
    links: z.array(z.string()).default([]),
    draft: z.boolean().optional().default(false),
  }),
});

const pages = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    cover: z.string().optional().default(""),
  }),
});

export const collections = { projects, pages };
