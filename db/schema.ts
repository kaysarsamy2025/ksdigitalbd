import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';
export const inquiries = sqliteTable('inquiries', {
 id: text('id').primaryKey(), name:text('name').notNull(), email:text('email').notNull(),
 service:text('service').notNull(), message:text('message').notNull(),
 budget:text('budget').notNull().default('Not specified'), timeline:text('timeline').notNull().default('Flexible'),
 status:text('status').notNull().default('new'), createdAt:integer('created_at').notNull(), consentAt:integer('consent_at').notNull()
});
export const siteSettings = sqliteTable('site_settings', { key:text('key').primaryKey(), value:text('value').notNull() });
