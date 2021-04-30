import lodash from 'lodash';

export const getFriends = async <T extends { id: string }>(
	user: T,
	getFollowing: (user: T) => Promise<T[]>
): Promise<T[]> => {
	const following = await getFollowing(user);

	return lodash.compact(
		await Promise.all(
			following.map(async (aFollowing) => {
				const followingOfFollowing = await getFollowing(aFollowing);

				if (
					followingOfFollowing.some(
						(aFollowingOfAFollowing) => aFollowingOfAFollowing.id === user.id
					)
				)
					return aFollowing;
			})
		)
	);
};

export const getTree = async <T extends { id: string }>(
	source: T,
	maxDepth: number,
	getFollowing: (user: T) => Promise<T[]>,
	sourceBranch: T[] = [],
	depth = 0
): Promise<T[][]> => {
	const tree: T[][] = [];
	const branch = sourceBranch.concat(source);

	if (depth < maxDepth) {
		const friends = await getFriends(source, getFollowing);

		for (let index = 0; index < friends.length; index++) {
			const friend = friends[index];
			const friendTree = await getTree(
				friend,
				maxDepth,
				getFollowing,
				branch,
				depth + 1
			);

			for (let index = 0; index < friendTree.length; index++) {
				const friendBranch = friendTree[index];

				tree.push(lodash.uniqBy(branch.concat(friendBranch.slice(1)), 'id'));
			}
		}

		return tree;
	} else {
		tree.push(lodash.uniqBy(branch.concat(source), 'id'));
		return tree;
	}
};

export const getSeparations = async <T extends { id: string }>(
	source: T,
	target: T,
	maxDepth: number,
	getFollowing: (user: T) => Promise<T[]>,
	targetPathsEntries: [string, T[]][] = [],
	depth = 0,
	path: T[] = []
): Promise<T[] | undefined> => {
	console.log(depth);

	if (depth === 0) {
		const targetPathsMaxDepth = 4;
		maxDepth -= targetPathsMaxDepth;

		const targetPaths: { [id: string]: T[] } = {};
		(await getTree(target, targetPathsMaxDepth, getFollowing)).forEach(
			(branch) => {
				const lastNode = lodash.last(branch);
				if (lastNode) targetPaths[lastNode.id] = branch.reverse();
			}
		);
		targetPathsEntries = Object.entries(targetPaths);
	}

	if (depth <= maxDepth) {
		const branch = targetPathsEntries
			.filter(([id]) => id === source.id)
			.reduce((a, b) => (a[1].length <= b[1].length ? a : b))?.[1];

		if (branch) return path.concat(branch);
		else {
			const idsInPath = path.map((account) => account.id);

			const sourceFriends = (await getFriends(source, getFollowing)).filter(
				(sourceFriend) => !idsInPath.includes(sourceFriend.id)
			);
			const targetFriends = await getFriends(target, getFollowing);
			const commonFriends = sourceFriends.filter((sourceFriend) =>
				targetFriends.some(
					(targetFriend) => sourceFriend.id === targetFriend.id
				)
			);

			if (!lodash.isEmpty(commonFriends)) {
				path.push(commonFriends[0]);
				return path;
			} else if (depth === 0) {
				let recursiveDepth = depth;

				while (recursiveDepth <= maxDepth) {
					for (let index = 0; index < sourceFriends.length; index++) {
						const sourceFriend = sourceFriends[index];

						const separations = await getSeparations(
							sourceFriend,
							target,
							recursiveDepth,
							getFollowing,
							targetPathsEntries,
							depth + 1,
							path
						);

						if (separations !== undefined && !lodash.isEmpty(commonFriends)) {
							path.push(...separations);
							return path;
						}
					}

					recursiveDepth += 1;
				}
			} else if (depth <= maxDepth) {
				for (let index = 0; index < sourceFriends.length; index++) {
					const sourceFriend = sourceFriends[index];

					const separations = await getSeparations(
						sourceFriend,
						target,
						maxDepth,
						getFollowing,
						targetPathsEntries,
						depth + 1,
						path
					);

					if (separations !== undefined && !lodash.isEmpty(commonFriends)) {
						path.push(...separations);
						return path;
					}
				}
			} else return undefined;
		}
	}
};

// export const checkBranch = async <T extends any>(
// 	branch: T[],
// 	getFollowing: (user: T) => Promise<T[]>
// ): Promise<boolean> => {
// 	let treeIsCorrect = true;

// 	for (let index = 1; index < branch.length; index++) {
// 		const account = branch[index];

// 		const accountFriends = await getFriends(account, getFollowing);

// 		if (treeIsCorrect) {
// 			treeIsCorrect = accountFriends.includes(branch[index - 1]);

// 			if (!treeIsCorrect) {
// 				return treeIsCorrect;
// 			}
// 		}
// 	}

// 	return treeIsCorrect;
// };

export * as simulation from './utils/buildAccounts';
export * as mastodon from './utils/mastodon';
