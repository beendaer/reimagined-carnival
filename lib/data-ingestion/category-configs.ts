export type CategoryConfig = {
  slug: string;
  displayName: string;
  requiredFields: string[];
  attributeKeys: string[];
};

export const CATEGORY_CONFIGS: Record<string, CategoryConfig> = {
  laptop: {
    slug: 'laptop',
    displayName: 'Laptops',
    requiredFields: ['make', 'model', 'price'],
    attributeKeys: ['cpu', 'ram', 'storage', 'battery_life']
  },
  tv: {
    slug: 'tv',
    displayName: 'TVs',
    requiredFields: ['make', 'model', 'price'],
    attributeKeys: ['screen_size', 'resolution', 'panel_type']
  },
  speaker: {
    slug: 'speaker',
    displayName: 'Speakers',
    requiredFields: ['make', 'model', 'price'],
    attributeKeys: ['power_output', 'frequency_response', 'connectivity']
  },
  microwave: {
    slug: 'microwave',
    displayName: 'Microwaves',
    requiredFields: ['make', 'model', 'price'],
    attributeKeys: ['capacity', 'wattage', 'preset_modes']
  },
  washing_machine: {
    slug: 'washing_machine',
    displayName: 'Washing Machines',
    requiredFields: ['make', 'model', 'price'],
    attributeKeys: [
      'reliability',
      'performance',
      'efficiency',
      'failure_rate',
      'repair_cost',
      'energy_cost'
    ]
  }
};
