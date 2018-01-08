const debug = process.env.NODE_ENV !== 'production'
const webpack = require('webpack')
const path = require('path')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const extractSass = new ExtractTextPlugin({
	filename: './public/css/[name].min.css',
	disable: process.env.NODE_ENV === 'development'
})

module.exports = {
	context: path.join(__dirname),
	devtool: debug ? 'inline-sourcemap' : null,
	entry: ['./src/js/index.js', './src/scss/index.scss'],
	devServer: { 
		inline: true, 
		port: 3000,
		publicPath: '/',
		contentBase: './public',
		hot: true,
		historyApiFallback: true
	},
	module: {
		loaders: [
			{
				test: /\.jsx?$/,
				exclude: /(node_modules|bower_components)/,
				loader: 'babel-loader',
				query: {
					presets: ['react', 'es2015', 'stage-0'],
					plugins: ['react-html-attrs', 'transform-class-properties', 'transform-decorators-legacy'],
				}
			},
			{
				test: /\.(s*)css$/,
				loaders: ['style-loader', 'css-loader', 'sass-loader', 'sass']
			},
			{
				test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
				loader: 'url-loader?limit=10000&mimetype=application/font-woff' },
			{ 
				test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, 
				loader: 'file-loader'
			} 
		],
		rules: [
			{
				test: /\.(s*)css$/,
				use: [
					{
						loader: 'style-loader' // creates style nodes from JS strings
					}, 
					{
						loader: 'sass-loader', // compiles Sass to CSS
					},
					{
						loader: 'css-loader', // translates CSS into CommonJS
					}
				]
			}
		],
		resolve: {
			extensions: ['', '.js', '.jsx', '.css', '.scss'],
			modulesDirectories: ['node_modules']
		}
	},
	output: {
		path: path.join(__dirname, 'public'),
		filename: './js/index.js'
	},
	plugins: debug ? [] : [
		new webpack.optimize.DedupePlugin(),
		new webpack.optimize.OccurenceOrderPlugin(),
		new webpack.optimize.UglifyJsPlugin({ mangle: false, sourcemap: false }),
		extractSass
	],
}
