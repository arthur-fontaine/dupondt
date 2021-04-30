import axios from 'axios';
import lodash from 'lodash';

import { Account } from '../../types/mastodon/accounts/Account';

// eslint-disable-next-line @typescript-eslint/no-var-requires
require('dotenv').config();

export const getFollowing = async (userId: string): Promise<Account[]> => {
	const response = await axios.get<Account[]>(
		`https://mastodon.social/api/v1/accounts/${userId}/following?limit=80`,
		{
			headers: {
				Authorization: `Bearer ${process.env.MASTODON_TOKEN}`
			}
		}
	);

	return response.data;
};

export const getFollowers = async (userId: string): Promise<Account[]> => {
	const response = await axios.get<Account[]>(
		`https://mastodon.social/api/v1/accounts/${userId}/followers?limit=80`,
		{
			headers: {
				Authorization: `Bearer ${process.env.MASTODON_TOKEN}`
			}
		}
	);

	return response.data;
};

export const getFriends = async (userId: string): Promise<Account[]> => {
	const following = await getFollowing(userId);

	return lodash.compact(
		await Promise.all(
			following.map(async (aFollowing) => {
				const followingOfFollowing = await getFollowing(aFollowing.id);

				if (
					followingOfFollowing.some(
						(aFollowingOfAFollowing) => aFollowingOfAFollowing.id === userId
					)
				)
					return aFollowing;
			})
		)
	);
};
