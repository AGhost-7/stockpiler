import React from 'react'
import $ from 'jquery'
import 'materialize-css'
import { Link } from 'react-router-dom'

import Menu from './menu'

export default class NavBar extends React.Component {
	

	componentDidMount() {
		$('.button-collapse').sideNav()
	}


	render() {
		return (
			<div>
				<div class='navbar-fixed'>
					<nav>
						<div class='nav-wrapper'>
							<Link to='/' class='brand-logo'>StockPiler</Link>
							<a href='#' data-activates='mobile-menu' class='button-collapse'>
								<i class='mi mi-face'>menu</i>
							</a>
							<Menu class='right hide-on-med-and-down'>
								{this.props.children}
							</Menu>
						</div>
					</nav>
				</div>
				<Menu class='side-nav' id='mobile-menu'>
					{this.props.children}
				</Menu>
			</div>
		)
	}

}
