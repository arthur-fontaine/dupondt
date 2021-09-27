import React from 'react';
import { useHistory } from 'react-router-dom';
import Button from '../../components/Button';
import { getSeparations } from '../../utils/dupondt';
import { Account } from '../../utils/dupondt/types/mastodon/accounts/Account';
import './../../style/simulation-find-the-path.scss';

interface IProps {
	[key: string]: any;
	location: RouterLocation<{
		accounts: Account[];
		followers: { [id: string]: Account[] };
		following: { [id: string]: Account[] };
	}>;
}

interface IState {
	path?: Account[];
}

class SelectPeople extends React.Component<IProps, IState> {
	accounts: Account[];
	following: { [id: string]: Account[] };
	followers: { [id: string]: Account[] };

	constructor(props: IProps) {
		super(props);

		if (this.props.location.state === undefined) location.replace('/');

		this.state = {};
		this.accounts = this.props.location.state.accounts;
		this.following = this.props.location.state.following;
		this.followers = this.props.location.state.followers;
	}

	render() {
		const findPath = async (start: Account, end: Account) =>
			await getSeparations(
				start,
				end,
				10,
				async (user: Account) => this.following[user.id]
			);

		return (
			<div className="find-path">
				<div>
					{this.state.path ? (
						<div className="path">
							{this.state.path.map((account, i) => {
								return (
									<div key={i}>
										<span className="path__divider"></span>
										<span className="path__display-name">
											{account.display_name}
										</span>
										<span className="path__divider"></span>
									</div>
								);
							})}
						</div>
					) : (
						<div className="no-path">There is no path</div>
					)}
					<Button
						value="Find the path between 2 random persons"
						onClick={async (e) => {
							const element = e.target as HTMLDivElement;
							const initialInnerText = element.innerText;
							element.innerText = 'Loading...';

							const p = async () => {
								try {
									const start =
										this.accounts[
											Math.floor(Math.random() * this.accounts.length)
										];
									const end =
										this.accounts[
											Math.floor(Math.random() * this.accounts.length)
										];

									const path = await findPath(start, end);

									this.setState({ path });

									console.log(this.state.path);
									element.innerText = initialInnerText;

									return;
								} catch (e) {
									await p();
								}
							};

							setTimeout(p, 0);
						}}
					/>
				</div>
			</div>
		);
	}
}

export default SelectPeople;
