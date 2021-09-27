import axios, { AxiosResponse } from 'axios';
import { Instagram } from '../types/instagram/Instagram';
import { getSeparations } from '../index';
import { Following } from '../types/instagram/following/Following';
import puppeteer from 'puppeteer';

// eslint-disable-next-line @typescript-eslint/no-var-requires
require('dotenv').config();

export const getId = async (username: string): Promise<string> => {
	const response = await axios.get<Instagram>(
		`https://www.instagram.com/${username}/?__a=1`
	);
	console.log(response.data);
	return response.data.graphql.user.id;
};

const getFollowing = async (
	userId: {
		id: string;
	},
	page: puppeteer.Page
): Promise<{ id: string }[]> => {
	console.log(userId.id);

	let data: Following | undefined;
	const followersId: { id: string }[] = [];

	do {
		await page.goto(
			`https://www.instagram.com/graphql/query/?query_hash=3dec7e2c57367ef3da3d987d89f9dbc8&variables=${encodeURIComponent(
				JSON.stringify({
					id: userId.id,
					include_reel: true,
					fetch_mutual: true,
					first: 50,
					after: data?.data.user.edge_follow.page_info.end_cursor
				})
			)}`
		);
		await page.waitForSelector('body');
		const body = await page.$('body');
		data = JSON.parse(
			await page.evaluate((el) => el.textContent, body)
		) as Following;

		followersId.push(
			...data.data.user.edge_follow.edges.map((node) => {
				return { id: node.node.id };
			})
		);
	} while (data.data.user.edge_follow.page_info.end_cursor !== null);

	return followersId;
};

const loginIG = async (browser: puppeteer.Browser) => {
	const page = await browser.newPage();
	await page.goto('https://instagram.com');

	await page.waitForSelector('input[name=username]');

	if (process.env.IG_USERNAME)
		await page.type('input[name=username]', process.env.IG_USERNAME);
	else throw 'No IG_USERNAME in .env file';

	if (process.env.IG_PW)
		await page.type('input[name=password]', process.env.IG_PW);
	else throw 'No IG_PW in .env file';

	await page.keyboard.press('Enter');
	await page.waitForNavigation();

	await page.close();

	return true;
};

(async () => {
	const browser = await puppeteer.launch({
		headless: false
	});

	await loginIG(browser);
	// console.log(await getFollowing({ id: '7390817294' }, page));

	const page = await browser.newPage();

	await getSeparations(
		{ id: '7390817294' },
		{ id: '22326145' },
		10,
		async (userId) => await getFollowing(userId, page)
	);
})();
