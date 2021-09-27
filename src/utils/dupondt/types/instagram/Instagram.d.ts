export interface Instagram {
	logging_page_id: string;
	show_suggested_profiles: boolean;
	show_follow_dialog: boolean;
	graphql: Graphql;
	toast_content_on_load: null;
	show_view_shop: boolean;
	profile_pic_edit_sync_props: null;
	always_show_message_button_to_pro_account: boolean;
}

interface Graphql {
	user: GraphqlUser;
}

interface GraphqlUser {
	biography: string;
	blocked_by_viewer: boolean;
	restricted_by_viewer: boolean;
	country_block: boolean;
	external_url: string;
	external_url_linkshimmed: string;
	edge_followed_by: EdgeFollowClass;
	fbid: string;
	followed_by_viewer: boolean;
	edge_follow: EdgeFollowClass;
	follows_viewer: boolean;
	full_name: string;
	has_ar_effects: boolean;
	has_clips: boolean;
	has_guides: boolean;
	has_channel: boolean;
	has_blocked_viewer: boolean;
	highlight_reel_count: number;
	has_requested_viewer: boolean;
	id: string;
	is_business_account: boolean;
	is_professional_account: boolean;
	is_joined_recently: boolean;
	business_category_name: null;
	overall_category_name: null;
	category_enum: null;
	category_name: null;
	is_private: boolean;
	is_verified: boolean;
	edge_mutual_followed_by: EdgeMutualFollowedBy;
	profile_pic_url: string;
	profile_pic_url_hd: string;
	requested_by_viewer: boolean;
	should_show_category: boolean;
	should_show_public_contacts: boolean;
	username: string;
	connected_fb_page: null;
	edge_felix_combined_post_uploads: EdgeFelixCombinedDraftUploadsClass;
	edge_felix_combined_draft_uploads: EdgeFelixCombinedDraftUploadsClass;
	edge_felix_video_timeline: EdgeFelixCombinedDraftUploadsClass;
	edge_felix_drafts: EdgeFelixCombinedDraftUploadsClass;
	edge_felix_pending_post_uploads: EdgeFelixCombinedDraftUploadsClass;
	edge_felix_pending_draft_uploads: EdgeFelixCombinedDraftUploadsClass;
	edge_owner_to_timeline_media: EdgeFelixCombinedDraftUploadsClass;
	edge_saved_media: EdgeFelixCombinedDraftUploadsClass;
	edge_media_collections: EdgeFelixCombinedDraftUploadsClass;
}

interface EdgeFelixCombinedDraftUploadsClass {
	count: number;
	page_info: PageInfo;
	edges: EdgeFelixCombinedDraftUploadsEdge[];
}

interface EdgeFelixCombinedDraftUploadsEdge {
	node: PurpleNode;
}

interface PurpleNode {
	__typename: Typename;
	id: string;
	shortcode: string;
	dimensions: Dimensions;
	display_url: string;
	edge_media_to_tagged_user: EdgeMediaTo;
	fact_check_overall_rating: null;
	fact_check_information: null;
	gating_info: null;
	sharing_friction_info: SharingFrictionInfo;
	media_overlay_info: null;
	media_preview: null | string;
	owner: Owner;
	is_video: boolean;
	accessibility_caption: string;
	edge_media_to_caption: EdgeMediaTo;
	edge_media_to_comment: EdgeFollowClass;
	comments_disabled: boolean;
	taken_at_timestamp: number;
	edge_liked_by: EdgeFollowClass;
	edge_media_preview_like: EdgeFollowClass;
	location: Location | null;
	thumbnail_src: string;
	thumbnail_resources: ThumbnailResource[];
}

declare enum Typename {
	GraphImage = 'GraphImage',
	GraphSidecar = 'GraphSidecar'
}

interface Dimensions {
	height: number;
	width: number;
}

interface EdgeFollowClass {
	count: number;
}

interface EdgeMediaTo {
	edges: EdgeMediaToCaptionEdge[];
}

interface EdgeMediaToCaptionEdge {
	node: FluffyNode;
}

interface FluffyNode {
	user?: NodeUser;
	x?: number;
	y?: number;
	text?: string;
}

interface NodeUser {
	full_name: string;
	id: string;
	is_verified: boolean;
	profile_pic_url: string;
	username: string;
}

interface Location {
	id: string;
	has_public_page: boolean;
	name: string;
	slug: string;
}

interface Owner {
	id: string;
	username: string;
}

interface SharingFrictionInfo {
	should_have_sharing_friction: boolean;
	bloks_app_url: null;
}

interface ThumbnailResource {
	src: string;
	config_width: number;
	config_height: number;
}

interface PageInfo {
	has_next_page: boolean;
	end_cursor: null | string;
}

interface EdgeMutualFollowedBy {
	count: number;
	edges: any[];
}
