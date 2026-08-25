<template>
  <span class="redacted" :class="{ 'is-block': block }" :title="tooltip">
    <template v-if="block">{{ bars }}</template>
    <template v-else>[DATOS EXPURGADOS]</template>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  // Nivel de clearance que haria falta para leer esto.
  level: { type: String, default: null },
  // Barra de bloques en vez de la leyenda; para campos largos como el lore.
  block: { type: Boolean, default: false },
  length: { type: Number, default: 32 },
  // Cuando lo tapo el dueno y no el clearance.
  byOwner: { type: Boolean, default: false }
})

const bars = computed(() => '█'.repeat(props.length))

const tooltip = computed(() => {
  if (props.byOwner) return 'Expurgado por el titular del expediente'
  return props.level
    ? `Requiere clearance ${props.level}`
    : 'Informacion expurgada'
})
</script>

<style scoped>
.redacted {
  display: inline-block;
  font-family: 'Consolas', monospace;
  font-size: 0.75rem;
  letter-spacing: 1px;
  color: #6a6a6a;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 0.1rem 0.4rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  cursor: help;
}

.redacted.is-block {
  color: #2a2a2a;
  background: #111;
  border-color: rgba(255, 255, 255, 0.05);
  letter-spacing: 0;
  white-space: normal;
  word-break: break-all;
  line-height: 1.4;
}
</style>
