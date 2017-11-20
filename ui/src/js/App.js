import React, { Component } from 'react'
import { Route } from 'react-router-dom'
import Header from './pages/Header'
import SPFooter from './pages/SPFooter'
import Home from './pages/Home'
import GetStarted from './pages/GetStarted'
import Login from './pages/Login'
import SignUp from './pages/SignUp'



class App extends Component {
	constructor() {
		super()

		this.state = {
			user: null,
		}
	}


	render() {
		return (
			<div className='app'>
				<Header></Header>
				<main>
					<Route exact path='/' component={Home}></Route>
					<Route path='/get-started' component={GetStarted}></Route>
					<Route path='/login' component={Login}></Route>
					<Route path='/sign-up' component={SignUp}></Route>
				</main>
				<SPFooter></SPFooter>
			</div>
		)
	}
}

export default App
