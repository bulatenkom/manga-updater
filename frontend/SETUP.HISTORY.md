# App

> Nodejs 20.11.1
> Quasar 2.14.4 (With use of Quasar CLI)
> VueUse 10.7.2

```bash
npm init quasar

✔ What would you like to build? › App with Quasar CLI, let's go!
✔ Project folder: … frontend
✔ Pick Quasar version: › Quasar v2 (Vue 3 | latest and greatest)
✔ Pick script type: › Typescript
✔ Pick Quasar App CLI variant: › Quasar App CLI with Vite 5 (BETA | next major version - v2)
✔ Package name: … manga-updater-frontend
✔ Project product name: (must start with letter if building mobile apps) … Manga updater
✔ Project description: … ...
✔ Author: … bulatenkom <bulatenkom@gmail.com>
✔ Pick a Vue component style: › Composition API with <script setup>
✔ Pick your CSS preprocessor: › Sass with SCSS syntax
✔ Check the features needed for your project: › ESLint
✔ Pick an ESLint preset: › Prettier

added 441 packages, and audited 442 packages in 22s

102 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities

To get started:

  cd frontend
  quasar dev # or: yarn quasar dev # or: npx quasar dev

Documentation can be found at: https://v2.quasar.dev
```

# VS Code

Extensions:
https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig
https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint
https://marketplace.visualstudio.com/items?itemName=wayou.vscode-todo-highlight
https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin
https://marketplace.visualstudio.com/items?itemName=Vue.volar
https://marketplace.visualstudio.com/items?itemName=vscode-icons-team.vscode-icons
https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode

> Note. Config files for formatter/codestyling resides in .vscode

# Eslint

Disable annoying rules in **.eslintrc.cjs**

```js
'@typescript-eslint/no-unused-vars': 'off'
```
