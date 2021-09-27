import faker from 'faker';
import lodash from 'lodash';

import { Account } from '../types/mastodon/accounts/Account';

const build = async (
	numberInhabitants = 5000,
	inhabitantCreatedCallback?: (account?: Account) => void
): Promise<{
	followers: {
		[id: string]: Account[];
	};
	following: {
		[id: string]: Account[];
	};
	accounts: Account[];
}> => {
	const accounts: Account[] = [];

	for (let index = 0; index < numberInhabitants; index++) {
		const id = index.toString();
		const firstName = faker.name.firstName();
		const lastName = faker.name.lastName();
		const username = faker.internet.userName(firstName, lastName);
		const created_at = faker.date.past();
		const avatar = faker.internet.avatar();
		const header = faker.image.abstract();
		const statuses_count = faker.datatype.number();
		const last_status_at = faker.date.past();

		const account = {
			id,
			username,
			acct: username,
			display_name: firstName + ' ' + lastName,
			locked: false,
			bot: false,
			discoverable: true,
			group: false,
			created_at,
			note: '',
			url: 'https://mastodon.social/@' + username,
			avatar,
			avatar_static: avatar,
			header,
			header_static: header,
			followers_count: 0,
			following_count: 0,
			statuses_count,
			last_status_at,
			emojis: [],
			fields: []
		};

		accounts.push(account);

		if (inhabitantCreatedCallback) inhabitantCreatedCallback(account);
	}

	const followers = <
		{
			[id: string]: Account[];
		}
	>{};

	const followings = <
		{
			[id: string]: Account[];
		}
	>{};

	accounts.forEach((account) => {
		followers[account.id] = lodash
			.shuffle(accounts)
			.slice(0, faker.datatype.number(500));
		account.followers_count = followers[account.id].length;

		followers[account.id].forEach((following) => {
			followings[following.id] = followings[following.id]
				? followings[following.id].concat(account)
				: [account];
		});
	});

	accounts.forEach((account, index) => {
		accounts[index].following_count = followings[account.id].length;
	});

	return { followers, following: followings, accounts };
};

export { build };
