import Layout from '@theme/Layout';
import { JSX } from 'react';
import Button from '../components/Button';
import { Info, FileText, Activity, AlertTriangle, CheckCircle, Grid, BarChart2, Code, PieChart } from 'lucide-react';
import React from 'react';

const CallToAction = () => {
  return (
    <div className="flex flex-col justify-center h-screen items-center">
      <h2 className="text-3xl md:text-4xl font-semibold text-center mb-6">
        Ease your data migration journey 🚀
      </h2>
      <p className="text-center mb-6 text-pretty">
        Follow our comprehensive guide to get up and running with Remorph in no time.
      </p>
      <Button
        variant="primary"
        link="/docs/installation"
        size="large"
        label="Start using remorph ✨"
        className="w-full p-4 font-mono md:w-auto bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:from-blue-600 hover:to-purple-600 transition-all duration-300"
      />
    </div>
  )
};

const Hero = () => {
  return (

    <div className="px-4 md:px-10 min-h-[calc(100vh-var(--ifm-navbar-height))] flex flex-col justify-center items-center w-full">
      {/* Logo Section */}
      <div className="m-2">
        <img src="img/logo.svg" alt="Remorph Logo" className="w-32 md:w-48" />
      </div>

      <h1 className="text-4xl md:text-5xl font-semibold text-center mb-6">
        Remorph - Assisted Migration Toolkit
      </h1>
      <p className="text-center text-gray-600 dark:text-gray-500 mb-4">
        Provided by <a href="https://github.com/databrickslabs">Databricks Labs</a>
      </p>
      <p className="text-lg text-center text-balance">
          Remorph is a comprehensive toolkit designed to facilitate seamless migrations to Databricks.
      </p>

      {/* Call to Action Buttons */}
      <div className="mt-12 flex flex-col space-y-4 md:flex-row md:space-y-0 md:space-x-4">
        <Button
          variant="secondary"
          outline={true}
          link="/docs/motivation"
          size="large"
          label={"Motivation"}
          className="w-full md:w-auto"
        />
        <Button
          variant="secondary"
          outline={true}
          link="/docs/installation"
          size="large"
          label={"Installation"}
          className="w-full md:w-auto"
        />
        <Button
          variant="secondary"
          outline={true}
          link="/docs/transpile_guide"
          size="large"
          label="Transpile Guide"
          className="w-full md:w-auto"
        />
        <Button
          variant="secondary"
          outline={true}
          link="/docs/reconcile"
          size="large"
          label="Reconcile Guide"
          className="w-full md:w-auto"
        />
          <Button
              variant="secondary"
              outline={true}
              link="/docs/assessment"
              size="large"
              label="Assessment Guide"
              className="w-full md:w-auto"
          />
          <Button
              variant="secondary"
              outline={true}
              link="/docs/demos"
              size="large"
              label="Demos"
              className="w-full md:w-auto"
          />
      </div>
    </div>
  );
};

export default function Home(): JSX.Element {
  return (
    <Layout>
      <main>
        <div className='flex justify-center mx-auto'>
          <div className='max-w-screen-lg'>
            <Hero />
            <CallToAction />
          </div>
        </div>
      </main>
    </Layout>
  );
}
