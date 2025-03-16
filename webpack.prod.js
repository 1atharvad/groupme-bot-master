const {merge} = require('webpack-merge')
const devConfig = require('./webpack.config')

module.exports = merge(devConfig, {
  mode: 'production',
  devtool: false,
})