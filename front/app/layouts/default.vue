<!-- eslint-disable vue/no-multiple-template-root -->
<!-- eslint-disable vue/html-indent -->
<template>
    <UHeader>
        <template #left>
            RIVO-IA
        </template>
        <template #right>
            <UButton>
                <template #icon>
                    <UIcon name="i-lucide-user" />
                </template>
            </UButton>
        </template>
    </UHeader>
    <UMain>
        <slot />
    </UMain>
    <UFooter>
        <template #left>
            <p class="text-sm text-muted">
                Built with Nuxt UI • © {{ new Date().getFullYear() }}
            </p>
        </template>
    </UFooter>
</template>

<script setup>
</script>
