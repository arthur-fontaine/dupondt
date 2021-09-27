export interface Followers {
	data: Data;
	status: string;
}

interface Data {
	user: User;
}

interface User {
	edge_followed_by: EdgeFollowedBy;
}

interface EdgeFollowedBy {
	count: number;
	page_info: PageInfo;
	edges: Edge[];
}

interface Edge {
	node: Node;
}

interface Node {
	id: string;
	username: string;
	full_name: string;
	profile_pic_url: string;
	is_private: boolean;
	is_verified: boolean;
	followed_by_viewer: boolean;
	follows_viewer: boolean;
	requested_by_viewer: boolean;
	reel: Reel;
}

interface Reel {
	id: string;
	expiring_at: number;
	has_pride_media: boolean;
	latest_reel_media: number;
	seen: null;
	owner: Owner;
}

interface Owner {
	__typename: Typename;
	id: string;
	profile_pic_url: string;
	username: string;
}

declare enum Typename {
	GraphUser = 'GraphUser'
}

interface PageInfo {
	has_next_page: boolean;
	end_cursor: string;
}
