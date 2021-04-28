export interface Account {
	id: string;
	username: string;
	acct: string;
	display_name: string;
	locked: boolean;
	bot: boolean;
	discoverable: boolean | null;
	group: boolean;
	created_at: Date;
	note: string;
	url: string;
	avatar: string;
	avatar_static: string;
	header: string;
	header_static: string;
	followers_count: number;
	following_count: number;
	statuses_count: number;
	last_status_at: Date | null;
	emojis: any[];
	fields: {
		name: string;
		value: string;
		verified_at: Date | null;
	}[];
}
