interface RouterLocation<State> {
	hash: string;
	key: string;
	pathname: string;
	search: string;
	state: State;
}
