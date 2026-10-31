# Mindrally Skills

One skills-only plugin containing all **265** skills from
[Mindrally/skills](https://github.com/Mindrally/skills), adapted for **Codex and
GitHub Copilot**. Version **0.1.0**.

Languages, frameworks, web and native applications, APIs, databases,
infrastructure, machine learning, testing, accessibility and engineering
practices remain separately discoverable. Closely related upstream skills keep
their identities so existing skill names remain available; invoke the most
specific matching skill instead of loading overlapping guides together.

## How progressive disclosure works

1. Skill metadata describes when to select the skill.
2. `SKILL.md` contains the essential project evidence, workflow, authority and
   completion contract.
3. Directly linked `references/` files contain conditional technical detail.
   Read only the reference matching the task and installed version.

Each source skill receives an individual accuracy review. Framework-specific
syntax, obsolete API examples, unsafe defaults and universal style mandates are
corrected or qualified. Documentation review and package validation do not prove
every framework example runs in a target project. Use its pinned dependencies
and appropriate project checks before reporting a behavioral result.

## Install and invoke

```bash
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
codex plugin add mindrally-skills@sealad886-codex-marketplace
```

```bash
copilot plugin marketplace add sealad886/sealad886-codex-marketplace
copilot plugin install mindrally-skills@sealad886-codex-marketplace
```

Refresh a previously registered marketplace before installation when necessary.
Start a fresh client task after installing. In Codex, an explicit invocation
looks like `$mindrally-skills:react` or `$mindrally-skills:python`.
Copilot discovers the same skill files through its plugin skill support.

Example requests:

- “Use the React skill to inspect this project's rendering and state flow.”
- “Use the FastAPI skill to implement this endpoint against our installed version.”
- “Use the SwiftUI skill to review the view's state ownership and accessibility.”

## Prerequisites and skill selection

The plugin supplies instructions. It does not install language runtimes,
frameworks, external services, CLI tools, credentials or client integrations.
Use the target project's existing environment and repository policies.
Capabilities differ between clients; a listed skill does not imply a tool or
service is available. Prefer current primary documentation for the installed
version over an unverified example.

All skills ship in the release. Individual enablement is a local user
preference: use the client's skill controls to disable unused technologies.
This package does not overwrite global settings or impose a shared enablement
profile on marketplace users.

## Provenance and contribution

Pinned upstream source: `7682ca77710e0971eab4e0ae5dddfa281aea0ba5`.
See [NOTICE.md](NOTICE.md) and [LICENSE](LICENSE) for Apache-2.0 attribution and
modification notices. Review records and source hashes live in the
[marketplace audit ledger](https://github.com/sealad886/sealad886-codex-marketplace/tree/main/docs/reviews/mindrally-skills).
The [security policy](SECURITY.md) describes authority and reporting boundaries.

Edit the owning skill and references. Keep source identity and the per-skill
audit record aligned. Place required workflow decisions in the entry point and
conditional detail in directly linked references; avoid duplicate implementations
or client-specific copies of skill content. Record a new primary-source review
when changing technical claims.

From the marketplace root, use its existing Python environment with bytecode
writing disabled:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_mindrally_skills.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_marketplace.py .
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_copilot_marketplace.py .
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_plugin.py plugins/mindrally-skills --layout source
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_distribution_bundle.py plugins/mindrally-skills
```

Run the regression suites specified by the marketplace contribution guide and
verify isolated native discovery and installation in both clients. Keep real
user settings and credentials untouched during package tests.

## Complete skill directory

| Skills A–Z | Skills A–Z | Skills A–Z |
| --- | --- | --- |
| [accessibility-a11y](skills/accessibility-a11y/SKILL.md) | [alpine-js](skills/alpine-js/SKILL.md) | [analytics-data-analysis](skills/analytics-data-analysis/SKILL.md) |
| [android-development](skills/android-development/SKILL.md) | [angular](skills/angular/SKILL.md) | [angular-development](skills/angular-development/SKILL.md) |
| [anime-js](skills/anime-js/SKILL.md) | [anthropic-claude-development](skills/anthropic-claude-development/SKILL.md) | [api-development](skills/api-development/SKILL.md) |
| [apollo-graphql](skills/apollo-graphql/SKILL.md) | [aspnet-core](skills/aspnet-core/SKILL.md) | [astro](skills/astro/SKILL.md) |
| [auth0-authentication](skills/auth0-authentication/SKILL.md) | [autogen-development](skills/autogen-development/SKILL.md) | [automl-hyperparameter-optimization](skills/automl-hyperparameter-optimization/SKILL.md) |
| [aws-development](skills/aws-development/SKILL.md) | [azure](skills/azure/SKILL.md) | [backend-development](skills/backend-development/SKILL.md) |
| [bash-scripting](skills/bash-scripting/SKILL.md) | [beautifulsoup-parsing](skills/beautifulsoup-parsing/SKILL.md) | [bitbucket-workflow](skills/bitbucket-workflow/SKILL.md) |
| [blazor](skills/blazor/SKILL.md) | [blender-python-addon](skills/blender-python-addon/SKILL.md) | [blockchain](skills/blockchain/SKILL.md) |
| [bootstrap](skills/bootstrap/SKILL.md) | [business-central-development](skills/business-central-development/SKILL.md) | [c-sharp](skills/c-sharp/SKILL.md) |
| [cheerio-parsing](skills/cheerio-parsing/SKILL.md) | [chrome-extension-development](skills/chrome-extension-development/SKILL.md) | [ci-cd-best-practices](skills/ci-cd-best-practices/SKILL.md) |
| [clean-architecture](skills/clean-architecture/SKILL.md) | [clean-code](skills/clean-code/SKILL.md) | [clerk-authentication](skills/clerk-authentication/SKILL.md) |
| [cloudflare-development](skills/cloudflare-development/SKILL.md) | [computer-vision-opencv](skills/computer-vision-opencv/SKILL.md) | [convex](skills/convex/SKILL.md) |
| [cpp](skills/cpp/SKILL.md) | [css](skills/css/SKILL.md) | [cypress](skills/cypress/SKILL.md) |
| [data-analysis-jupyter](skills/data-analysis-jupyter/SKILL.md) | [data-analyst](skills/data-analyst/SKILL.md) | [data-jupyter-python](skills/data-jupyter-python/SKILL.md) |
| [deep-learning](skills/deep-learning/SKILL.md) | [deep-learning-python](skills/deep-learning-python/SKILL.md) | [deep-learning-pytorch](skills/deep-learning-pytorch/SKILL.md) |
| [deno-typescript](skills/deno-typescript/SKILL.md) | [design-systems](skills/design-systems/SKILL.md) | [devops](skills/devops/SKILL.md) |
| [django-python](skills/django-python/SKILL.md) | [django-rest-api-development](skills/django-rest-api-development/SKILL.md) | [docker](skills/docker/SKILL.md) |
| [dotnet](skills/dotnet/SKILL.md) | [drizzle-orm](skills/drizzle-orm/SKILL.md) | [drupal-development](skills/drupal-development/SKILL.md) |
| [elasticsearch-best-practices](skills/elasticsearch-best-practices/SKILL.md) | [electron-development](skills/electron-development/SKILL.md) | [elixir](skills/elixir/SKILL.md) |
| [embedded-stm32](skills/embedded-stm32/SKILL.md) | [esbuild-bundler](skills/esbuild-bundler/SKILL.md) | [ethereum](skills/ethereum/SKILL.md) |
| [expo-react-native-javascript-best-practices](skills/expo-react-native-javascript-best-practices/SKILL.md) | [expo-react-native-typescript](skills/expo-react-native-typescript/SKILL.md) | [express-typescript](skills/express-typescript/SKILL.md) |
| [fastapi-microservices-serverless](skills/fastapi-microservices-serverless/SKILL.md) | [fastapi-python](skills/fastapi-python/SKILL.md) | [fastify-typescript](skills/fastify-typescript/SKILL.md) |
| [figma-integration](skills/figma-integration/SKILL.md) | [firebase-development](skills/firebase-development/SKILL.md) | [flask-python](skills/flask-python/SKILL.md) |
| [flutter](skills/flutter/SKILL.md) | [fortran](skills/fortran/SKILL.md) | [fpga](skills/fpga/SKILL.md) |
| [framer-motion](skills/framer-motion/SKILL.md) | [front-end-developer](skills/front-end-developer/SKILL.md) | [game-development](skills/game-development/SKILL.md) |
| [gamemaker-gml](skills/gamemaker-gml/SKILL.md) | [gcp-development](skills/gcp-development/SKILL.md) | [general-best-practices](skills/general-best-practices/SKILL.md) |
| [ghost](skills/ghost/SKILL.md) | [git-workflow](skills/git-workflow/SKILL.md) | [gitflow](skills/gitflow/SKILL.md) |
| [github-workflow](skills/github-workflow/SKILL.md) | [gitlab-workflow](skills/gitlab-workflow/SKILL.md) | [go](skills/go/SKILL.md) |
| [go-api-development](skills/go-api-development/SKILL.md) | [go-backend-microservices](skills/go-backend-microservices/SKILL.md) | [google-adk](skills/google-adk/SKILL.md) |
| [graalvm](skills/graalvm/SKILL.md) | [graphql](skills/graphql/SKILL.md) | [graphql-development](skills/graphql-development/SKILL.md) |
| [grpc-development](skills/grpc-development/SKILL.md) | [gsap](skills/gsap/SKILL.md) | [harmony-arkts](skills/harmony-arkts/SKILL.md) |
| [hono-typescript](skills/hono-typescript/SKILL.md) | [html](skills/html/SKILL.md) | [htmx](skills/htmx/SKILL.md) |
| [internationalization-i18n](skills/internationalization-i18n/SKILL.md) | [ionic](skills/ionic/SKILL.md) | [java](skills/java/SKILL.md) |
| [java-quarkus-development](skills/java-quarkus-development/SKILL.md) | [java-spring-development](skills/java-spring-development/SKILL.md) | [jax-best-practices](skills/jax-best-practices/SKILL.md) |
| [jest](skills/jest/SKILL.md) | [julia](skills/julia/SKILL.md) | [jwt-security](skills/jwt-security/SKILL.md) |
| [kafka-development](skills/kafka-development/SKILL.md) | [koa-typescript](skills/koa-typescript/SKILL.md) | [kotlin-development](skills/kotlin-development/SKILL.md) |
| [kubernetes](skills/kubernetes/SKILL.md) | [kysely](skills/kysely/SKILL.md) | [langchain-development](skills/langchain-development/SKILL.md) |
| [laravel](skills/laravel/SKILL.md) | [laravel-development](skills/laravel-development/SKILL.md) | [lerna](skills/lerna/SKILL.md) |
| [less-best-practices](skills/less-best-practices/SKILL.md) | [llamaindex-development](skills/llamaindex-development/SKILL.md) | [llm](skills/llm/SKILL.md) |
| [localization-l10n](skills/localization-l10n/SKILL.md) | [logging-best-practices](skills/logging-best-practices/SKILL.md) | [lottie](skills/lottie/SKILL.md) |
| [lua](skills/lua/SKILL.md) | [machine-learning](skills/machine-learning/SKILL.md) | [matplotlib-best-practices](skills/matplotlib-best-practices/SKILL.md) |
| [medusa-development](skills/medusa-development/SKILL.md) | [meta-prompt](skills/meta-prompt/SKILL.md) | [micronaut](skills/micronaut/SKILL.md) |
| [microservices](skills/microservices/SKILL.md) | [modern-web-development](skills/modern-web-development/SKILL.md) | [mongodb-development](skills/mongodb-development/SKILL.md) |
| [monitoring-guidelines](skills/monitoring-guidelines/SKILL.md) | [monorepo](skills/monorepo/SKILL.md) | [monorepo-tamagui](skills/monorepo-tamagui/SKILL.md) |
| [motion](skills/motion/SKILL.md) | [mqtt-development](skills/mqtt-development/SKILL.md) | [mysql-best-practices](skills/mysql-best-practices/SKILL.md) |
| [nestjs-clean-typescript](skills/nestjs-clean-typescript/SKILL.md) | [netlify-development](skills/netlify-development/SKILL.md) | [network-troubleshooting](skills/network-troubleshooting/SKILL.md) |
| [nextauth-authentication](skills/nextauth-authentication/SKILL.md) | [nextjs-react-redux-typescript-cursor-rules](skills/nextjs-react-redux-typescript-cursor-rules/SKILL.md) | [nextjs-react-typescript](skills/nextjs-react-typescript/SKILL.md) |
| [nextjs-typescript-tailwindcss-supabase](skills/nextjs-typescript-tailwindcss-supabase/SKILL.md) | [nlp-natural-language-processing](skills/nlp-natural-language-processing/SKILL.md) | [nodejs-development](skills/nodejs-development/SKILL.md) |
| [numpy-best-practices](skills/numpy-best-practices/SKILL.md) | [nuxtjs-vue-typescript](skills/nuxtjs-vue-typescript/SKILL.md) | [nx](skills/nx/SKILL.md) |
| [oauth-implementation](skills/oauth-implementation/SKILL.md) | [observability-guidelines](skills/observability-guidelines/SKILL.md) | [odoo-development](skills/odoo-development/SKILL.md) |
| [onchainkit](skills/onchainkit/SKILL.md) | [openai-api-development](skills/openai-api-development/SKILL.md) | [optimized-nextjs-typescript](skills/optimized-nextjs-typescript/SKILL.md) |
| [pandas-best-practices](skills/pandas-best-practices/SKILL.md) | [parcel-bundler](skills/parcel-bundler/SKILL.md) | [performance-optimization](skills/performance-optimization/SKILL.md) |
| [phoenix](skills/phoenix/SKILL.md) | [php-development](skills/php-development/SKILL.md) | [pixi-js](skills/pixi-js/SKILL.md) |
| [playwright](skills/playwright/SKILL.md) | [playwright-cursor-rules](skills/playwright-cursor-rules/SKILL.md) | [pnpm](skills/pnpm/SKILL.md) |
| [postcss-best-practices](skills/postcss-best-practices/SKILL.md) | [postgresql-best-practices](skills/postgresql-best-practices/SKILL.md) | [pr-review](skills/pr-review/SKILL.md) |
| [prisma](skills/prisma/SKILL.md) | [prisma-development](skills/prisma-development/SKILL.md) | [puppeteer-automation](skills/puppeteer-automation/SKILL.md) |
| [pwa-development](skills/pwa-development/SKILL.md) | [pyspark-etl](skills/pyspark-etl/SKILL.md) | [python](skills/python/SKILL.md) |
| [python-cybersecurity-tool-development](skills/python-cybersecurity-tool-development/SKILL.md) | [python-odoo-cursor-rules](skills/python-odoo-cursor-rules/SKILL.md) | [python-testing](skills/python-testing/SKILL.md) |
| [python-uv](skills/python-uv/SKILL.md) | [pytorch](skills/pytorch/SKILL.md) | [quarkus](skills/quarkus/SKILL.md) |
| [rabbitmq-development](skills/rabbitmq-development/SKILL.md) | [react](skills/react/SKILL.md) | [react-native-cursor-rules](skills/react-native-cursor-rules/SKILL.md) |
| [react-native-r3f](skills/react-native-r3f/SKILL.md) | [react-query](skills/react-query/SKILL.md) | [react-router-v7](skills/react-router-v7/SKILL.md) |
| [readme-best-practices](skills/readme-best-practices/SKILL.md) | [redis-best-practices](skills/redis-best-practices/SKILL.md) | [redux-toolkit](skills/redux-toolkit/SKILL.md) |
| [remix](skills/remix/SKILL.md) | [responsive-design](skills/responsive-design/SKILL.md) | [rest-api-django](skills/rest-api-django/SKILL.md) |
| [robocorp-cursor-rules](skills/robocorp-cursor-rules/SKILL.md) | [rollup-bundler](skills/rollup-bundler/SKILL.md) | [ros2-robotics](skills/ros2-robotics/SKILL.md) |
| [rspec](skills/rspec/SKILL.md) | [rtl-internationalization](skills/rtl-internationalization/SKILL.md) | [ruby](skills/ruby/SKILL.md) |
| [ruby-rails](skills/ruby-rails/SKILL.md) | [rust](skills/rust/SKILL.md) | [salesforce-development](skills/salesforce-development/SKILL.md) |
| [salesforce-dx](skills/salesforce-dx/SKILL.md) | [sanity](skills/sanity/SKILL.md) | [sass-best-practices](skills/sass-best-practices/SKILL.md) |
| [scikit-learn-best-practices](skills/scikit-learn-best-practices/SKILL.md) | [scipy-best-practices](skills/scipy-best-practices/SKILL.md) | [scrapy-web-scraping](skills/scrapy-web-scraping/SKILL.md) |
| [scss-best-practices](skills/scss-best-practices/SKILL.md) | [security-best-practices](skills/security-best-practices/SKILL.md) | [security-devsecops](skills/security-devsecops/SKILL.md) |
| [selenium-automation](skills/selenium-automation/SKILL.md) | [seo-best-practices](skills/seo-best-practices/SKILL.md) | [sequelize](skills/sequelize/SKILL.md) |
| [serverless](skills/serverless/SKILL.md) | [shopify](skills/shopify/SKILL.md) | [shopify-theme-development-guidelines](skills/shopify-theme-development-guidelines/SKILL.md) |
| [snowflake-cortex-ai](skills/snowflake-cortex-ai/SKILL.md) | [snowflake-data-engineering](skills/snowflake-data-engineering/SKILL.md) | [snowflake-snowpark-dbt](skills/snowflake-snowpark-dbt/SKILL.md) |
| [solana](skills/solana/SKILL.md) | [solidity](skills/solidity/SKILL.md) | [spring-boot](skills/spring-boot/SKILL.md) |
| [spring-framework](skills/spring-framework/SKILL.md) | [sql-best-practices](skills/sql-best-practices/SKILL.md) | [storybook](skills/storybook/SKILL.md) |
| [stripe](skills/stripe/SKILL.md) | [styled-components-best-practices](skills/styled-components-best-practices/SKILL.md) | [supabase](skills/supabase/SKILL.md) |
| [supabase-development](skills/supabase-development/SKILL.md) | [svelte](skills/svelte/SKILL.md) | [sveltekit](skills/sveltekit/SKILL.md) |
| [swift](skills/swift/SKILL.md) | [swiftui-development](skills/swiftui-development/SKILL.md) | [swr](skills/swr/SKILL.md) |
| [systemverilog](skills/systemverilog/SKILL.md) | [tailwindcss](skills/tailwindcss/SKILL.md) | [tanstack-query](skills/tanstack-query/SKILL.md) |
| [tanstack-router](skills/tanstack-router/SKILL.md) | [tanstack-start](skills/tanstack-start/SKILL.md) | [tauri-development](skills/tauri-development/SKILL.md) |
| [technical-writing](skills/technical-writing/SKILL.md) | [tensorflow-deep-learning](skills/tensorflow-deep-learning/SKILL.md) | [terraform](skills/terraform/SKILL.md) |
| [testing](skills/testing/SKILL.md) | [three-js](skills/three-js/SKILL.md) | [transformers-huggingface](skills/transformers-huggingface/SKILL.md) |
| [trpc](skills/trpc/SKILL.md) | [turbopack-bundler](skills/turbopack-bundler/SKILL.md) | [turborepo](skills/turborepo/SKILL.md) |
| [typeorm](skills/typeorm/SKILL.md) | [typescript](skills/typescript/SKILL.md) | [ui-design](skills/ui-design/SKILL.md) |
| [unity](skills/unity/SKILL.md) | [ux-design](skills/ux-design/SKILL.md) | [vercel-development](skills/vercel-development/SKILL.md) |
| [viewcomfy-api-rules](skills/viewcomfy-api-rules/SKILL.md) | [vite](skills/vite/SKILL.md) | [vue-pinia](skills/vue-pinia/SKILL.md) |
| [vue-typescript](skills/vue-typescript/SKILL.md) | [vuejs-typescript-best-practices](skills/vuejs-typescript-best-practices/SKILL.md) | [web-development](skills/web-development/SKILL.md) |
| [web-scraping](skills/web-scraping/SKILL.md) | [webpack-bundler](skills/webpack-bundler/SKILL.md) | [websocket-development](skills/websocket-development/SKILL.md) |
| [woocommerce](skills/woocommerce/SKILL.md) | [wordpress](skills/wordpress/SKILL.md) | [zod-schema-validation](skills/zod-schema-validation/SKILL.md) |
| [zustand-state-management](skills/zustand-state-management/SKILL.md) |  |  |
