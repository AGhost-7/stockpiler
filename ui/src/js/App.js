import React, { Component } from 'react'
import { Route } from 'react-router-dom'
import Header from './components/Header'
import SPFooter from './components/SPFooter'
import Home from './components/Home'
import GetStarted from './components/GetStarted'
import Login from './components/Login'
import SignUp from './components/SignUp'



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
