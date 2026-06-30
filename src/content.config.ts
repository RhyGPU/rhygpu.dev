import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const commitSchema = z.object({
  hash: z.string(),
  title: z.string(),
  repo: z.string().optional(),
  url: z.string().url().optional()
});

const mediaSchema = z.object({
  title: z.string(),
  type: z.enum(['screenshot', 'video', 'diagram', 'placeholder']).default('placeholder'),
  src: z.string().optional(),
  alt: z.string().optional(),
  caption: z.string(),
  status: z.enum(['available', 'planned']).default('planned')
});

const demoLinkSchema = z.object({
  title: z.string(),
  url: z.string(),
  caption: z.string().optional()
});

const devlogs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/devlogs' }),
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
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    featured: z.boolean().default(false),
    order: z.number().default(99),
    subtitle: z.string().optional(),
    status: z.string(),
    summary: z.string(),
    repo: z.string().url().optional(),
    demo: z.string().url().optional(),
    devlog: z.string().optional(),
    stack: z.array(z.string()).default([]),
    highlights: z.array(z.string()).default([]),
    architecture: z.array(z.string()).default([]),
    media: z.array(mediaSchema).default([]),
    demoLinks: z.array(demoLinkSchema).default([]),
    proofNotes: z.array(z.string()).default([]),
    showHighlightsPanel: z.boolean().default(true),
    tags: z.array(z.string()).default([])
  })
});

export const collections = { devlogs, projects };
