import { defineCollection, z } from 'astro:content';

const commitSchema = z.object({
  hash: z.string(),
  title: z.string(),
  repo: z.string().optional(),
  url: z.string().url().optional()
});

const devlogs = defineCollection({
  type: 'content',
  schema: z.object({
    number: z.string(),
    title: z.string(),
    subtitle: z.string().optional(),
    slug: z.string(),
    project: z.string(),
    date: z.coerce.date(),
    status: z.enum(['draft', 'published']).default('draft'),
    summary: z.string(),
    tags: z.array(z.string()).default([]),
    commits: z.array(commitSchema).default([])
  })
});

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    status: z.string(),
    summary: z.string(),
    repo: z.string().url().optional(),
    tags: z.array(z.string()).default([])
  })
});

export const collections = { devlogs, projects };
