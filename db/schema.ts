import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';
export const inquiries = sqliteTable('inquiries', {
 id: text('id').primaryKey(), name:text('name').notNull(), email:text('email').notNull(),
 service:text('service').notNull(), message:text('message').notNull(),
 budget:text('budget').notNull().default('Not specified'), timeline:text('timeline').notNull().default('Flexible'),
 status:text('status').notNull().default('new'), createdAt:integer('created_at').notNull(), consentAt:integer('consent_at').notNull()
});
export const siteSettings = sqliteTable('site_settings', { key:text('key').primaryKey(), value:text('value').notNull() });

export const cmsEntries = sqliteTable('cms_entries', {
 id:text('id').primaryKey(), kind:text('kind').notNull(), slug:text('slug').notNull().unique(),
 title:text('title').notNull(), summary:text('summary').notNull().default(''), body:text('body').notNull().default(''),
 price:text('price').notNull().default(''), image:text('image').notNull().default(''), video:text('video').notNull().default(''),
 status:text('status').notNull().default('draft'), updatedAt:integer('updated_at').notNull()
});
export const cmsMedia = sqliteTable('cms_media', {
 id:text('id').primaryKey(), name:text('name').notNull(), type:text('type').notNull(), size:integer('size').notNull(), createdAt:integer('created_at').notNull()
});
