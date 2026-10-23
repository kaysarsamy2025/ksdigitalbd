CREATE TABLE `cms_entries` (
	`id` text PRIMARY KEY NOT NULL,
	`kind` text NOT NULL,
	`slug` text NOT NULL,
	`title` text NOT NULL,
	`summary` text DEFAULT '' NOT NULL,
	`body` text DEFAULT '' NOT NULL,
	`price` text DEFAULT '' NOT NULL,
	`image` text DEFAULT '' NOT NULL,
	`video` text DEFAULT '' NOT NULL,
	`status` text DEFAULT 'draft' NOT NULL,
	`updated_at` integer NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `cms_entries_slug_unique` ON `cms_entries` (`slug`);--> statement-breakpoint
CREATE TABLE `cms_media` (
	`id` text PRIMARY KEY NOT NULL,
	`name` text NOT NULL,
	`type` text NOT NULL,
	`size` integer NOT NULL,
	`created_at` integer NOT NULL
);
