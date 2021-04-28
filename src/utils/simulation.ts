import { Account } from '../../types/mastodon-api/accounts/Account';
import { getSeparations, checkBranch, simulation } from '../index';

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

	if (separation) console.log(await checkBranch(separation, getFollowing));
})();
