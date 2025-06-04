import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    'motivation',
    'installation',
    {
      type: 'category',
      label: 'Assessment',
      items: [
        'assessment/profiler',
        'assessment/analyzer',
      ],
    },
    {
      type: 'doc',
      id: 'transpile/index',
      label: 'Transpiler',
    },
    {
      type: 'doc',
      id: 'reconcile/index',
      label: 'Reconciler',
    }
  ],
};

export default sidebars;
