module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/essential',
    '@vue/airbnb',
  ],
  parserOptions: {
    ecmaVersion: 2020,
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'import/prefer-default-export': 'off',
    'max-len': 'off',
    'no-plusplus': 'off',
    camelcase: 'off',
    'no-unused-vars': 'off',
    'vars-on-top': 'off',
    'no-var': 'off',
    radix: 'off',
    'no-redeclare': 'off',
    'prefer-arrow-callback': 'off',

  },
};
