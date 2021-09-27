import { Account } from '../types/mastodon/accounts/Account';
import { getSeparations, simulation } from '../index';

(async () => {
	const { following, accounts } = await simulation.build();

	const getFollowing = async (user: Account) => {
		return following[user.id];
	};

	const separation = await getSeparations(
		accounts[1],
		accounts[2],
		10,
		getFollowing
	);
	console.log(separation);
})();
