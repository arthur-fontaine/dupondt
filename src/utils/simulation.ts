import { Account } from '../../types/mastodon/accounts/Account';
import { getSeparations, simulation } from '../index';

const getFollowing = async (user: Account) => {
	return simulation.following[user.id];
};

(async () => {
	const separation = await getSeparations(
		simulation.accounts[1],
		simulation.accounts[2],
		10,
		getFollowing
	);
	console.log(separation);
})();
