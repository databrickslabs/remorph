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
      type: 'category',
      label: 'Transpiler',
      link: {
        type: 'doc',
        id: 'transpile/index',
      },
      items: [
        'transpile/pluggable_transpilers',
      ],
    },
    {
      type: 'category',
      label: 'Reconciler',
      link: {
        type: 'doc',
        id: 'reconcile/index',
      },
      items: [
        'reconcile/reconcile_configuration',
        'reconcile/recon_notebook',
        'reconcile/example_config',
        'reconcile/dataflow_example',
        'reconcile/faq'
      ],
    }
  ],
};

export default sidebars;
